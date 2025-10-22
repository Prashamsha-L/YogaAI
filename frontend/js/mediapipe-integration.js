// mediapipe-integration.js
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

  // stability + smoothing state
  let prevAngles = null;
  let stagnantCount = 0;
  const STAGNANT_THRESHOLD = 15; 
  const TOLERANCE = 8;           
  const SMOOTH_FRAMES = 5;      
  let angleHistory = [];
  let lastSentTime = 0;
  const SEND_COOLDOWN = 1200;

  let isSending = false;

  let poseHistory = [];
  const POSE_WINDOW = 15;  
  const POSE_THRESHOLD = 0.6;

  window.showSkeleton = true;

  


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
    // safe indexing inside angleABC guards against missing landmarks
    return [
      angleABC(lm[ID.LEFT_SHOULDER], lm[ID.LEFT_ELBOW], lm[ID.LEFT_WRIST]),    // left_elbow
      angleABC(lm[ID.RIGHT_SHOULDER], lm[ID.RIGHT_ELBOW], lm[ID.RIGHT_WRIST]),// right_elbow
      angleABC(lm[ID.LEFT_ELBOW], lm[ID.LEFT_SHOULDER], lm[ID.LEFT_HIP]),     // left_shoulder
      angleABC(lm[ID.RIGHT_ELBOW], lm[ID.RIGHT_SHOULDER], lm[ID.RIGHT_HIP]), // right_shoulder
      angleABC(lm[ID.LEFT_HIP], lm[ID.LEFT_KNEE], lm[ID.LEFT_ANKLE]),        // left_knee
      angleABC(lm[ID.RIGHT_HIP], lm[ID.RIGHT_KNEE], lm[ID.RIGHT_ANKLE]),     // right_knee
      angleABC(lm[ID.LEFT_SHOULDER], lm[ID.LEFT_HIP], lm[ID.LEFT_KNEE]),     // left_hip
      angleABC(lm[ID.RIGHT_SHOULDER], lm[ID.RIGHT_HIP], lm[ID.RIGHT_KNEE])   // right_hip
    ];
  }

  async function sendAngles(angles) {
    // Debounce: send only when cooldown passed
    const now = Date.now();
    if (now - lastSentTime < SEND_COOLDOWN) return;
    if (isSending) return;
    lastSentTime = now;
    isSending = true;

    try {
      // const levelSelectEl = document.getElementById("levelSelect");
      // const selectedLevel = levelSelectEl ? levelSelectEl.value : "beginner";

      // console.log("Sending angles:", angles, "Level:", selectedLevel);


      // console.log("Angles -> backend:", angles, "Level:", selectedLevel);
      const res = await fetch("http://127.0.0.1:8002/predict_pose", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ angles })
      });
      if (!res.ok) {
        console.error("Backend error:", res.status);
        return;
      }
      const data = await res.json();
      console.log("Backend response:", data);
      updateLabel(data);
    } catch (err) {
      console.error("Error sending angles:", err);
    } finally {
    isSending = false;
  }
  }
  function smoothPose(poseName) {
  poseHistory.push(poseName);
  if (poseHistory.length > POSE_WINDOW) poseHistory.shift();

  const counts = {};
  for (const p of poseHistory) counts[p] = (counts[p] || 0) + 1;

  let maxCount = 0, dominantPose = poseName;
  for (const [p, count] of Object.entries(counts)) {
    if (count > maxCount) {
      maxCount = count;
      dominantPose = p;
    }
  }

  // Only return if it exceeds threshold
  if (maxCount / poseHistory.length >= POSE_THRESHOLD) return dominantPose;
  return "No Pose Detected"; // otherwise keep old pose / show loading
}


  function updateLabel(data) {
    const labelEl = document.getElementById("pose-label");
    if (!labelEl) return;

    if (data.pose && data.pose !== "No angles received" && !data.pose.startsWith("Error:")) {
      const poseName = data.pose;

       if (poseName !== "No Pose Detected" && poseName !== "Loading...") {
      labelEl.textContent = `Pose: ${poseName}`;
      labelEl.style.color = "#fff";
      labelEl.style.backgroundColor = "#000";
      labelEl.style.fontSize = "30px";

            if (poseName && poseName !== "No Pose Detected") {
        // Capture thumbnail image from canvas (safe fallback if id differs)
        let canvasEl = document.getElementById('output_canvas');
        let imgData = null;
        try {
          if (canvasEl) {
            // use smaller thumbnail size for storage by drawing into an offscreen canvas
            const thumbW = 320; // thumbnail width
            const thumbH = Math.round((canvasEl.height / canvasEl.width) * thumbW);
            const off = document.createElement('canvas');
            off.width = thumbW;
            off.height = thumbH;
            const offCtx = off.getContext('2d');
            offCtx.drawImage(canvasEl, 0, 0, canvasEl.width, canvasEl.height, 0, 0, thumbW, thumbH);
            imgData = off.toDataURL('image/png');
          }
        } catch (e) {
          console.warn('Could not capture image:', e);
        }

        
        // ensure sessionResults is an object of arrays
        let sessionResults = JSON.parse(sessionStorage.getItem("sessionResults") || "{}");
        if (!sessionResults[poseName]) sessionResults[poseName] = [];

        if (data.corrections) {
          const joints = Object.values(data.corrections);
          if (joints.length > 0) {
            // count how many joints are correct (green)
            const correct = joints.filter(c => c === "green").length;
            const frameAccuracy = (correct / joints.length) * 100;

            // push object with accuracy + image + timestamp
            sessionResults[poseName].push({
              accuracy: frameAccuracy,
              image: imgData,
              ts: Date.now()
            });
          }
        }

        // save back to sessionStorage
        sessionStorage.setItem("sessionResults", JSON.stringify(sessionResults));
        sessionStorage.setItem("detectedPose", poseName);
      }

      
//----------------
  
      if (data.feedback && data.feedback.length) {
        const fb = data.feedback.join(" | ");
        labelEl.textContent += " - " + fb;
      }
      // sessionStorage.setItem('detectedPose', poseName);
      window.latestCorrections = data.corrections || {};
    }
    } else {
      labelEl.textContent = "Pose: No Pose Detected";
      window.latestCorrections = {};
    }
  }

  function initializeMediaPipe() {
    const videoElement = document.getElementById('webcam');
    const canvasElement = document.getElementById('output_canvas');
    const canvasCtx = canvasElement.getContext('2d');

    canvasElement.width = 1280;
    canvasElement.height = 720;

    // Create Pose instance
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
    return criticalJoints.every(i => {
    const lm = landmarks[i];
    if (!lm) return false;  // missing
    if (typeof lm.visibility !== "number") return lm.visibility > 0.6;
    // fallback: check joint inside frame
    return lm.x >= 0 && lm.x <= 1 && lm.y >= 0 && lm.y <= 1;
  });
}


    // Results handler
    pose.onResults((results) => {
      canvasCtx.save();
      canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);
      canvasCtx.drawImage(results.image, 0, 0, canvasElement.width, canvasElement.height);

       if (!results.poseLandmarks || results.poseLandmarks.length < 25) {
      //  updateLabel({ pose: "No Pose Detected" });
      const labelEl = document.getElementById("pose-label");
      if (labelEl) labelEl.textContent = "Pose: No pose detected";
      window.latestCorrections = {};
      canvasCtx.restore();
      return;
  }

    if (!isFullBodyVisible(results.poseLandmarks)) {
    const labelEl = document.getElementById("pose-label");
    if (labelEl) labelEl.textContent = "";
    
    const frame = canvasCtx.getImageData(0, 0, canvasElement.width, 50);
let avg = 0;
for (let i = 0; i < frame.data.length; i += 4) {
    avg += (frame.data[i] + frame.data[i + 1] + frame.data[i + 2]) / 3;
}
avg /= (frame.data.length / 4);

const textColor = avg > 128 ? "black" : "white";
const bgColor = avg > 128 ? "rgba(255,255,255,0.5)" : "rgba(0,0,0,0.5)";

const text = "Full body not visible, please step back";
canvasCtx.font = "15px Arial";
canvasCtx.textAlign = "center";

// Padding and rectangle height
const paddingX = 10;  // horizontal padding
const paddingY = 10;  // vertical padding (increase this to make it taller)
const textWidth = canvasCtx.measureText(text).width;
const rectWidth = textWidth + paddingX * 2;
const rectHeight = 25 + paddingY * 2; // original 25 + paddingY*2 makes it taller

// Draw rectangle centered
canvasCtx.fillStyle = bgColor;
canvasCtx.fillRect(
    canvasElement.width / 2 - rectWidth / 2,
    30 - rectHeight / 2,  // center rectangle vertically around text y-position
    rectWidth,
    rectHeight
);

// Draw text in the middle of the rectangle
canvasCtx.fillStyle = textColor;
canvasCtx.fillText(text, canvasElement.width / 2, 30);



     



     
    
    window.latestCorrections = {};
    canvasCtx.restore();
    return;
  }
         if (window.showSkeleton) {
        drawConnectors(canvasCtx, results.poseLandmarks, POSE_CONNECTIONS, { color: '#AAAAAA', lineWidth: 1.5 });
         }

        // ANGLES + SMOOTHING
        const rawAngles = buildAngleVector(results.poseLandmarks);
        const angles = smoothAngles(rawAngles);

        // const landmarksVector = buildFullLandmarkVector(results.poseLandmarks);

        console.log("Angles:", angles.map(a => a.toFixed(2)));


        // STABILITY CHECK (relaxed)
        if (prevAngles) {
          let stable = true;
          for (let i = 0; i < angles.length; i++) {
            if (Math.abs(angles[i] - prevAngles[i]) > TOLERANCE) {
              stable = false;
              break;
            }
          }

          if (stable) {
            stagnantCount++;
          } else {
            // relaxed decay to tolerate small shakes
            stagnantCount = Math.max(0, stagnantCount - 1);
          }
        }

        // Save for next frame
        prevAngles = [...angles];

        // WHEN STABLE: send once (debounced) to backend which returns corrections
        if (stagnantCount >= STAGNANT_THRESHOLD) {
          sendAngles(angles);
        } else {
          // keep last label visible; only show "Loading..." while still collecting stability
          const labelEl = document.getElementById("pose-label");
          if (labelEl) labelEl.textContent = "Pose: Loading...";
        }

        // DRAW corrections overlay (if backend returned any)
        if (window.showSkeleton) {
        const corrections = window.latestCorrections || {};
        const jointMap = {
          left_elbow: 13,
          right_elbow: 14,
          left_shoulder: 11,
          right_shoulder: 12,
          left_knee: 25,
          right_knee: 26,
          left_hip: 23,
          right_hip: 24
        };

        // Draw small neutral circles for every mapped joint (for visibility)
        for (const [joint, id] of Object.entries(jointMap)) {
          const lm = results.poseLandmarks[id];
          if (!lm) continue;
          canvasCtx.beginPath();
          canvasCtx.arc(lm.x * canvasElement.width, lm.y * canvasElement.height, 2, 0, 2 * Math.PI);
          canvasCtx.fillStyle = "#FFFFFF";
          canvasCtx.fill();
        }

        // Overlay colored joints + recolor connected bones
        for (const joint in corrections) {
          const id = jointMap[joint];
          if (id === undefined) continue;
          const lm = results.poseLandmarks[id];
          if (!lm) continue;
          const color = corrections[joint] === "green" ? "#00FF00" : "#FF0000";

          // colored joint
          canvasCtx.beginPath();
          canvasCtx.arc(lm.x * canvasElement.width, lm.y * canvasElement.height, 2, 0, 2 * Math.PI);
          canvasCtx.fillStyle = color;
          canvasCtx.fill();

          // recolor bones connected to this landmark
          const connections = POSE_CONNECTIONS.filter(([a, b]) => a === id || b === id);
          for (const [a, b] of connections) {
            const pa = results.poseLandmarks[a];
            const pb = results.poseLandmarks[b];
            if (!pa || !pb) continue;
            canvasCtx.beginPath();
            canvasCtx.moveTo(pa.x * canvasElement.width, pa.y * canvasElement.height);
            canvasCtx.lineTo(pb.x * canvasElement.width, pb.y * canvasElement.height);
            canvasCtx.strokeStyle = color;
            canvasCtx.lineWidth = 1.5;
            canvasCtx.stroke();
          }
        }}
      

      canvasCtx.restore();
    });

    // Camera helper from @mediapipe/camera_utils
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
        .then(() => {
          console.log("Camera started");
          document.getElementById("startBtn").textContent = "Running...";
        })
        .catch((err) => {
          console.error("Camera start failed:", err);
          isRunning = false;
          document.getElementById("startBtn").textContent = "Start";
        });
    }
  }

  function stopDetection() {
    if (isRunning) {
      isRunning = false;
      // stop camera tracks safely
      try {
        if (camera && camera.video && camera.video.srcObject) {
          camera.video.srcObject.getTracks().forEach(t => t.stop());
        }
      } catch (e) { console.warn("Error stopping camera:", e); }
      document.getElementById("startBtn").textContent = "Start";

      const currentPose = document.getElementById("pose-label").textContent.replace("Pose: ", "").trim();
      if (currentPose && currentPose !== "Loading..." && currentPose !== "No pose detected") {
        sessionStorage.setItem('detectedPose', currentPose);
      }
    }
  }

  document.addEventListener('DOMContentLoaded', () => {
    initializeMediaPipe();
    document.getElementById("startBtn").addEventListener("click", startDetection);
    document.getElementById("stopBtn").addEventListener("click", () => {
      stopDetection();
      window.location.href = 'result.html';
    });
  });

})();
