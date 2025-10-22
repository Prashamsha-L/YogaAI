(() => {
  const ID = {
    LEFT_SHOULDER: 11, RIGHT_SHOULDER: 12,
    LEFT_ELBOW: 13, RIGHT_ELBOW: 14,
    LEFT_WRIST: 15, RIGHT_WRIST: 16,
    LEFT_HIP: 23, RIGHT_HIP: 24,
    LEFT_KNEE: 25, RIGHT_KNEE: 26,
    LEFT_ANKLE: 27, RIGHT_ANKLE: 28
  };

  let camera = null;
  let pose = null;
  let isRunning = false;

  // smoothing + stability
  let prevAngles = null;
  let stagnantCount = 0;
  const STAGNANT_THRESHOLD = 15; 
  const TOLERANCE = 8;           
  const SMOOTH_FRAMES = 5;      
  let angleHistory = [];

  // Pose smoothing
  let poseHistory = [];
  const POSE_WINDOW = 15;  
  const POSE_THRESHOLD = 0.6;

  // Surya Namaskar steps
  const suryaPoses = [
    "Pranamasana", "Hasta Uttanasana", "Padahastasana", 
    "Ashwa Sanchalanasana", "Chaturanga Dandasana", 
    "Ashtanaga Namaskar", "Bhujangasana", "Adho Mukha Svanasana",
    "Ashwa Sanchalanasana - right"
  ];
  let currentPoseIndex = 0;
  let autoAdvanceOnDetect = true;

  const sessionResults = JSON.parse(sessionStorage.getItem("sessionResults")) || {};
  window.onSuryaDetected = function(detectedPose) {
    if (!detectedPose) return;

    const expected = suryaPoses[currentPoseIndex];
    if (!expected) return;

    sessionResults[expected] = sessionResults[expected] || [];
    sessionResults[expected].push({ pose: detectedPose, accuracy: 100, feedback: [] });

    sessionStorage.setItem("sessionResults", JSON.stringify(sessionResults));

    if (autoAdvanceOnDetect && detectedPose.toLowerCase() === expected.toLowerCase()) {
        setTimeout(() => nextPose(), 700);
    }
};

  function smoothAngles(newAngles) {
    angleHistory.push(newAngles);
    if (angleHistory.length > SMOOTH_FRAMES) angleHistory.shift();
    const avg = new Array(newAngles.length).fill(0);
    for (const frame of angleHistory) {
      for (let i = 0; i < frame.length; i++) avg[i] += frame[i];
    }
    return avg.map(v => v / angleHistory.length);
  }

  function angleABC(A, B, C) {
    if (!A || !B || !C) return 0;
    const BAx = A.x - B.x, BAy = A.y - B.y;
    const BCx = C.x - B.x, BCy = C.y - B.y;
    const dot = BAx * BCx + BAy * BCy;
    const magBA = Math.hypot(BAx, BAy);
    const magBC = Math.hypot(BCx, BCy);
    if (magBA === 0 || magBC === 0) return 0;
    let cos = dot / (magBA * magBC);
    cos = Math.max(-1, Math.min(1, cos));
    return Math.acos(cos) * (180 / Math.PI);
  }

  function buildAngleVector(lm) {
    return [
      angleABC(lm[ID.LEFT_SHOULDER], lm[ID.LEFT_ELBOW], lm[ID.LEFT_WRIST]),
      angleABC(lm[ID.RIGHT_SHOULDER], lm[ID.RIGHT_ELBOW], lm[ID.RIGHT_WRIST]),
      angleABC(lm[ID.LEFT_ELBOW], lm[ID.LEFT_SHOULDER], lm[ID.LEFT_HIP]),
      angleABC(lm[ID.RIGHT_ELBOW], lm[ID.RIGHT_SHOULDER], lm[ID.RIGHT_HIP]),
      angleABC(lm[ID.LEFT_HIP], lm[ID.LEFT_KNEE], lm[ID.LEFT_ANKLE]),
      angleABC(lm[ID.RIGHT_HIP], lm[ID.RIGHT_KNEE], lm[ID.RIGHT_ANKLE]),
      angleABC(lm[ID.LEFT_SHOULDER], lm[ID.LEFT_HIP], lm[ID.LEFT_KNEE]),
      angleABC(lm[ID.RIGHT_SHOULDER], lm[ID.RIGHT_HIP], lm[ID.RIGHT_KNEE])
    ];
  }

  async function sendSuryaAngles(angles) {
    try {
      const res = await fetch("http://127.0.0.1:8002/predict_surya", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ angles: angles })
      });
      const data = await res.json();

      // Update label + corrections
      updateSuryaLabel(data);

      // ✅ Store result in sessionResults
      const expectedPose = suryaPoses[currentPoseIndex];
      if (expectedPose) {
        sessionResults[expectedPose] = data.pose;
        sessionStorage.setItem("sessionResults", JSON.stringify(sessionResults));
      }

      // Auto advance if detected matches expected
      if (autoAdvanceOnDetect && data.pose.toLowerCase() === expectedPose.toLowerCase()) {
        setTimeout(() => {
          if (currentPoseIndex < suryaPoses.length - 1) currentPoseIndex++;
        }, 700);
      }

      // Notify outer page
      if (window.onSuryaDetected && typeof window.onSuryaDetected === "function") {
        window.onSuryaDetected(data.pose);
      }
    } catch (err) {
      console.error("Error sending angles:", err);
    }
  }

  function updateSuryaLabel(data) {
    const labelEl = document.getElementById("pose-label");
    if (!labelEl) return;
    if (data.pose && data.pose !== "No Pose Detected") {
      labelEl.textContent = `Detected: ${data.pose}`;
      if (data.feedback && data.feedback.length) {
        labelEl.textContent += " — " + data.feedback.join(" | ");
      }
    } else {
      labelEl.textContent = "Detected: No Pose";
    }
    window.latestCorrections = data.corrections || {};
  }

  function initializeMediaPipe() {
    const videoElement = document.getElementById('webcam');
    const canvasElement = document.getElementById('output_canvas');
    const canvasCtx = canvasElement.getContext('2d');

    canvasElement.width = 1280;
    canvasElement.height = 720;

    pose = new Pose({
      locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/pose/${file}`
    });
    pose.setOptions({
      modelComplexity: 1,
      smoothLandmarks: true,
      minDetectionConfidence: 0.5,
      minTrackingConfidence: 0.5
    });

    function isFullBodyVisible(landmarks) {
      const criticalJoints = [11, 12, 13, 14, 23, 24, 25, 26];
      return criticalJoints.every(i => landmarks[i] && landmarks[i].x >= 0 && landmarks[i].x <= 1 && landmarks[i].y >= 0 && landmarks[i].y <= 1);
    }

    pose.onResults((results) => {
      canvasCtx.save();
      canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);
      canvasCtx.drawImage(results.image, 0, 0, canvasElement.width, canvasElement.height);

      if (!results.poseLandmarks || !isFullBodyVisible(results.poseLandmarks)) {
        updateSuryaLabel({ pose: "No Pose Detected" });
        window.latestCorrections = {};
        canvasCtx.restore();
        return;
      }

      // drawConnectors(canvasCtx, results.poseLandmarks, POSE_CONNECTIONS, { color: '#AAAAAA', lineWidth: 1.5 });
      if (showSkeleton) {
  drawConnectors(canvasCtx, results.poseLandmarks, POSE_CONNECTIONS,{ color: '#AAAAAA', lineWidth: 1.5 });
  // drawLandmarks(canvasCtx, results.poseLandmarks);
}

      const rawAngles = buildAngleVector(results.poseLandmarks);
      const angles = smoothAngles(rawAngles);

      if (prevAngles) {
        let stable = true;
        for (let i = 0; i < angles.length; i++) {
          if (Math.abs(angles[i] - prevAngles[i]) > TOLERANCE) stable = false;
        }
        stagnantCount = stable ? stagnantCount + 1 : Math.max(0, stagnantCount - 1);
      }
      prevAngles = [...angles];

      if (stagnantCount >= STAGNANT_THRESHOLD) {
        sendSuryaAngles(angles);
        stagnantCount = 0;
      }

      // Draw joints + corrections overlay
      const corrections = window.latestCorrections || {};
      const jointMap = {
        left_elbow: 13, right_elbow: 14,
        left_shoulder: 11, right_shoulder: 12,
        left_knee: 25, right_knee: 26,
        left_hip: 23, right_hip: 24
      };
      for (const [joint, id] of Object.entries(jointMap)) {
        const lm = results.poseLandmarks[id];
        if (!lm) continue;
        canvasCtx.beginPath();
        canvasCtx.arc(lm.x * canvasElement.width, lm.y * canvasElement.height, 2, 0, 2 * Math.PI);
        canvasCtx.fillStyle = corrections[joint] === "green" ? "#00FF00" : "#FF0000";
        canvasCtx.fill();
      }

      canvasCtx.restore();
    });

    camera = new Camera(videoElement, {
      onFrame: async () => { if (isRunning) await pose.send({ image: videoElement }); },
      width: 640,
      height: 480
    });
  }

  function startDetection() {
    if (!isRunning) {
      isRunning = true;
      camera.start()
        .then(() => document.getElementById("startBtn").textContent = "Running...")
        .catch(err => { console.error(err); isRunning = false; document.getElementById("startBtn").textContent = "Start"; });
    }
  }

  function stopDetection() {
    if (isRunning) {
      isRunning = false;
      try {
        if (camera && camera.video && camera.video.srcObject) {
          camera.video.srcObject.getTracks().forEach(t => t.stop());
        }
      } catch (e) {}
      document.getElementById("startBtn").textContent = "Start";
    }
  }

  document.addEventListener('DOMContentLoaded', () => {
    initializeMediaPipe();
    document.getElementById("startBtn").addEventListener("click", startDetection);
    document.getElementById("stopBtn").addEventListener("click", () => {
      stopDetection();
      window.location.href = 'surya_result.html';
    });
  });
})();
