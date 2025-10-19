from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import pickle
import numpy as np
import logging
import sys

app = FastAPI()

# Enable CORS so frontend JS can call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# logging.basicConfig( stream=sys.stdout,level=logging.INFO)
# logger = logging.getLogger("yoga-pose")

logger = logging.getLogger("uvicorn")  
logger.setLevel(logging.INFO)

# Angle-based model (existing)
with open("yoga_pose_xgb.pkl", "rb") as f:
    angle_model = pickle.load(f)

# Surya Namaskara model
with open("surya_namaskar.pkl", "rb") as f:
    surya_model = pickle.load(f)

# Surya pose labels
surya_labels = {
    0: "Adho Mukha Svanasana",
    1: "Ashtanaga Namaskar",
    2: "Ashwa Sanchalanasana",
    3: "Ashwa Sanchalasana - right",
    4: "Bhujangasana",
    5: "Chaturanga Dandasana",
    6: "Hasta Uttanasana",
    7: "Padahastasana",
    8: "Pranamasana"
}


CONFIDENCE_THRESHOLD = 0.70  # start permissive; raise later if needed
VARIANCE_THRESHOLD = 5.0     # small variance -> likely neutral/standing
MIN_ANGLE_COUNT = 8          # expect 8 angle features


pose_labels =  {
    0: 'Adho Mukha Svanasana', 1: 'Ananda balasana', 2: 'Anantasana', 3: 'Anjaneyasana',
    4: 'Ardha Chakrasana', 5: 'Ardha Chandrasana', 6: 'Ardha Matsyendrasana', 7: 'Ardha Uttasana',
    8: 'Baddha Konasana', 9: 'Balasana', 10: 'Bhujangasana', 11: 'Bitilasana',
    12: 'Dandasana', 13: 'Dhanurasana', 14: 'Gomukhasana', 15: 'Halasana',
    16: 'Kapotasana', 17: 'Malasana', 18: 'Marjariasana', 19: 'Mayurasana',
    20: 'Natarajasana', 21: 'Padmasana', 22: 'Parighasana', 23: 'Paripurna Navasana',
    24: 'Parivritta Trikonasana', 25: 'Phalakasana', 26: 'Setu Bandha Sarvangasana', 27: 'Svarga dvidasana', 28: 'Tadasana Samasthiti', 29: 'Tadasana Urdhva Baddha Hastasana', 30: 'Tadasana Urdhva Hastasana', 31: 'Tittibhasana', 32: 'Urdhva Dandasana', 33: 'Urdhva Dhanurasana', 34: 'Utkata Konasana', 35: 'Utkatasana', 36: 'Uttana shishosana', 37: 'Uttanasana', 38: 'Utthita Hasta Padangusthasana', 39: 'Utthita Hasta Padasana', 40: 'Utthita Parsvakonasana', 41: 'Utthita Trikonasana', 42: 'Vajrasana', 43: 'Vasisthasana', 44: 'Virabhadrasana One', 45: 'Virabhadrasana Two', 46: 'Virabhadrasana Three', 47: 'Visvamitrasana', 48: 'Vrichikasana', 49: 'Vrkshasana'
}

from correction import check_pose
    
joint_names = [
            "left_elbow", "right_elbow",
            "left_shoulder", "right_shoulder",
            "left_knee", "right_knee",
            "left_hip", "right_hip"
        ]
@app.post("/predict_pose")
async def predict_pose(request: Request):
    data = await request.json()
    angles = data.get("angles", [])

    if not angles or len(angles) < MIN_ANGLE_COUNT:
        return JSONResponse({"pose": "No Pose Detected", "confidence": 0.0})

    # convert to numpy floats safely
    try:
        arr = np.array(angles, dtype=float).reshape(1, -1)
        raw = arr.flatten()
    except Exception:
        return JSONResponse({"pose": "No Pose Detected", "confidence": 0.0})

    # check for NaNs or all zeros
    if np.isnan(raw).any() or np.all(raw == 0):
        return JSONResponse({"pose": "No Pose Detected", "confidence": 0.0})

    # small-variance check (very little movement or almost flat angles)

    if np.var(raw) < VARIANCE_THRESHOLD:
        return JSONResponse({"pose": "No Pose Detected", "confidence": 0.0})

    try:
        if hasattr(angle_model, "predict_proba"):
            proba = angle_model.predict_proba(arr)[0]
            prediction = int(np.argmax(proba))
            confidence = float(np.max(proba))
        else:
            prediction = int(angle_model.predict(arr)[0])
            confidence = None
        
        pose_name = pose_labels.get(prediction, "Unknown Pose")

    # print("Received angles:", angles)


    # Case 1: No pose detected (angles empty or all zero)
    # if not angles or sum(1 for a in angles if a == 0.1) > len(angles) // 2:
    #     return JSONResponse({"pose": "No Pose Detected", "confidence": 0.0})


    # try:
    #     # Convert angles list to numpy array
    #     X = np.array(angles).reshape(1, -1)

    #     # Case 2: Use confidence threshold
    #     if hasattr(angle_model, "predict_proba"):
    #         proba = angle_model.predict_proba(X)[0]
    #         prediction = np.argmax(proba)
    #         confidence = float(np.max(proba))  
    #     else:
    #         prediction = angle_model.predict(X)[0]
    #         confidence = None  

    #     pose_name = pose_labels.get(prediction, "Unknown Pose")

    #     # NEW CHECK 1: Variance (neutral or invalid posture)
    #     if np.var(angles) < 50:
    #         return JSONResponse({"pose": "No Pose Detected", "confidence": confidence})

    #     # NEW CHECK 2: Higher confidence
    #     if confidence is not None and confidence < 0.85:
    #         return JSONResponse({"pose": "No Pose Detected", "confidence": confidence})



        # print(f"[PREDICTION]: {pose_name}")
        # print(f"[CONFIDENCE]: {confidence}")
        # Apply confidence threshold (optional)


        if confidence is not None and confidence < CONFIDENCE_THRESHOLD:
            print(f"Low confidence ({confidence:.2f}), returning No Pose")
            return JSONResponse({"pose": "No Pose Detected", "confidence": confidence})

        
        corrections, feedback = check_pose(pose_name, raw.tolist(), joint_names)
        wrong_joints = sum(1 for c in corrections.values() if c != "green")

        logger.info("\n===== Pose Prediction =====")
        logger.info(f"Predicted Pose : {pose_name}")
        logger.info(f"Angles         : {[round(a,2) for a in raw.tolist()]}")
        logger.info(f"Joint Status   : {corrections}")
        logger.info(f"Confidence     : {confidence:.2f}" if confidence else "Confidence: None")
        logger.info(f"Wrong Joints   : {wrong_joints}")
        logger.info(f"Feedback       : {feedback}")
        logger.info("============================\n")

        if wrong_joints >= 3:  
            return JSONResponse({
        "pose": "No Pose Detected",
        "confidence": confidence,
        "corrections": corrections,
        "feedback": feedback
    })

        # print(f"Predicted Pose: {pose_name} ({confidence:.2f})" if confidence else f"Predicted Pose: {pose_name}")

        # if angles:
        #     corrections, feedback = check_pose(pose_name, angles, joint_names)
        # else:
        #     corrections, feedback = {}, [] 

        return JSONResponse({
        "pose": pose_name,
        "confidence": confidence,
        "angles": angles,
        "corrections": corrections,
        "feedback": feedback
    })
       
    except Exception as e:
        print(f"Error during prediction: {str(e)}")
        return JSONResponse({"pose": f"Error: {str(e)}", "confidence": 0.0})

@app.post("/predict_surya")
async def predict_surya(request: Request):
    data = await request.json()
    angles = data.get("angles", [])

    if not angles or len(angles) < MIN_ANGLE_COUNT:
        return JSONResponse({"pose": "No Pose Detected", "confidence": 0.0})

    try:
        arr = np.array(angles, dtype=float).reshape(1, -1)
        raw = arr.flatten()
    except Exception:
        return JSONResponse({"pose": "No Pose Detected", "confidence": 0.0})

    if np.isnan(raw).any() or np.all(raw == 0):
        return JSONResponse({"pose": "No Pose Detected", "confidence": 0.0})

    if np.var(raw) < VARIANCE_THRESHOLD:
        return JSONResponse({"pose": "No Pose Detected", "confidence": 0.0})

    try:
        if hasattr(surya_model, "predict_proba"):
            proba = surya_model.predict_proba(arr)[0]
            prediction = int(np.argmax(proba))
            confidence = float(np.max(proba))
        else:
            prediction = int(surya_model.predict(arr)[0])
            confidence = None

        pose_name = surya_labels.get(prediction, "Unknown Pose")

        if confidence is not None and confidence < CONFIDENCE_THRESHOLD:
            return JSONResponse({"pose": "No Pose Detected", "confidence": confidence})

        corrections, feedback = check_pose(pose_name, raw.tolist(), joint_names)
        wrong_joints = sum(1 for c in corrections.values() if c != "green")

        if wrong_joints >= 3:
            return JSONResponse({
                "pose": "No Pose Detected",
                # "confidence": confidence,
                # "corrections": corrections,
                # "feedback": feedback
            })

        return JSONResponse({
            "pose": pose_name,
            # "confidence": confidence,
            # "angles": angles,
            # "corrections": corrections,
            # "feedback": feedback
        })

    except Exception as e:
        return JSONResponse({"pose": f"Error: {str(e)}", "confidence": 0.0})



# @app.post("/predict_pose")
# async def predict_pose(request: Request):
#     try:
#         data = await request.json()
#         angles = data.get("angles", [])

#         # Basic validation
#         if not angles or len(angles) < MIN_ANGLE_COUNT:
#             return JSONResponse({"pose": "No Pose Detected", "confidence": 0.0})

#         arr = np.array(angles, dtype=float).reshape(1, -1)
#         raw = arr.flatten()

#         # Invalid angles check
#         if np.isnan(raw).any() or np.all(raw == 0):
#             return JSONResponse({"pose": "No Pose Detected", "confidence": 0.0})

#         # Small variance → neutral pose
#         if np.var(raw) < VARIANCE_THRESHOLD:
#             return JSONResponse({"pose": "No Pose Detected", "confidence": 0.0})

#         # Predict pose
#         if hasattr(angle_model, "predict_proba"):
#             proba = angle_model.predict_proba(arr)[0]
#             prediction = int(np.argmax(proba))
#             confidence = float(np.max(proba))
#         else:
#             prediction = int(angle_model.predict(arr)[0])
#             confidence = None

#         pose_name = pose_labels.get(prediction, "Unknown Pose")

#         # Confidence threshold check
#         if confidence is not None and confidence < CONFIDENCE_THRESHOLD:
#             return JSONResponse({"pose": "No Pose Detected", "confidence": confidence})

#         # Pose correction feedback
#         corrections, feedback = check_pose(pose_name, raw.tolist(), joint_names)
#         wrong_joints = sum(1 for c in corrections.values() if c != "green")

#         # If too many wrong joints → reject pose
#         if wrong_joints >= 3:
#             return JSONResponse({
#                 "pose": "No Pose Detected",
#                 "confidence": confidence,
#                 "corrections": corrections,
#                 "feedback": feedback
#             })

#         # Return successful prediction
#         return JSONResponse({
#             "pose": pose_name,
#             "confidence": confidence,
#             "angles": angles,
#             "corrections": corrections,
#             "feedback": feedback
#         })

#     except Exception as e:
#         # Catch all errors
#         return JSONResponse({"pose": f"Error: {str(e)}", "confidence": 0.0})
