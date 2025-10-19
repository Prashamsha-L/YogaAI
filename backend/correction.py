import time
import pyttsx3
import numpy as np
engine = pyttsx3.init()
engine.setProperty("rate", 150)   
engine.setProperty("volume", 1)   

def speak_feedback(messages):
    """Convert feedback messages into speech."""
    for msg in messages:
        engine.say(msg)
    engine.runAndWait()

POSE_SYMMETRIC = {
    "Pranamasana":{
        "left_elbow": 30, "right_elbow": 30,
        "left_shoulder": 25, "right_shoulder": 25,
        "left_knee": 180, "right_knee": 180,
        "left_hip": 180, "right_hip": 180
    },
# --------------------------------------------
    "Padahastasana":{
        "left_elbow": 180, "right_elbow": 180,
        "left_shoulder": 135, "right_shoulder": 135,
        "left_knee": 175, "right_knee": 175,
        "left_hip": 21, "right_hip": 21
    },
    "Hasta Uttanasana":{
        "left_elbow": 160, "right_elbow": 160,
        "left_shoulder": 150, "right_shoulder": 150,
        "left_knee": 175, "right_knee": 175,
        "left_hip": 130, "right_hip": 130
    },
    "Chaturanga Dandasana":{
        "left_elbow": 90, "right_elbow": 90,
        "left_shoulder": 5, "right_shoulder": 5,
        "left_knee": 180, "right_knee": 180,
        "left_hip": 180, "right_hip": 180
    },
    "Ashwa Sanchalasana - right":{
        "left_elbow": 160, "right_elbow": 160,
        "left_shoulder": 25, "right_shoulder": 25,
        "left_knee": 85, "right_knee": 125,
        "left_hip": 75, "right_hip": 150
    },
    "Ashwa Sanchalanasana":{
        "left_elbow": 175, "right_elbow": 175 ,
        "left_shoulder": 18, "right_shoulder": 18,
        "left_knee": 50, "right_knee": 140,
        "left_hip": 68, "right_hip": 120
    },
    "Ashtanaga Namaskar":{
        "left_elbow": 30, "right_elbow": 30,
        "left_shoulder": 10, "right_shoulder": 10,
        "left_knee": 115, "right_knee": 115,
        "left_hip": 90, "right_hip": 90
    },

    "Adho Mukha Svanasana": {
        "left_elbow": 165, "right_elbow": 180,
        "left_shoulder": 170, "right_shoulder": 170,
        "left_knee": 175, "right_knee": 175,
        "left_hip": 50, "right_hip": 50
    },
    "Ananda balasana": {
        "left_elbow": 165, "right_elbow": 160,
        "left_shoulder": 80, "right_shoulder": 80,
        "left_knee": 115, "right_knee": 120,
        "left_hip": 25, "right_hip": 35
    },
    "Anantasana": {
        "left_elbow": 53, "right_elbow": 175,
        "left_shoulder": 162, "right_shoulder": 103,
        "left_knee": 178, "right_knee": 178,
        "left_hip": 173, "right_hip": 59
    },
    "Ardha Chakrasana": {
        "left_elbow": 165, "right_elbow": 165,
        "left_shoulder": 160, "right_shoulder": 160,
        "left_knee": 175, "right_knee": 175,
        "left_hip": 115, "right_hip": 125
    },
    "Ardha Uttasana": {
        "left_elbow": 165, "right_elbow": 170,
        "left_shoulder": 60, "right_shoulder": 70,
        "left_knee": 175, "right_knee": 175,
        "left_hip": 77, "right_hip": 75
    },

    "Balasana": {
        "left_elbow": 165, "right_elbow": 150,
        "left_shoulder": 155, "right_shoulder": 150,
        "left_knee": 40, "right_knee": 35,
        "left_hip": 30, "right_hip": 25
    },
    "Baddha Konasana":  {"left_elbow": 175, "right_elbow": 175, "left_shoulder": 3, "right_shoulder": 3, "left_knee": 16, "right_knee": 16, "left_hip": 75, "right_hip": 75},

    "Bhujangasana": {
        "left_elbow": 168, "right_elbow": 164,
        "left_shoulder": 14, "right_shoulder": 12,
        "left_knee": 170, "right_knee": 176,
        "left_hip": 121, "right_hip": 117
    },
    "Bitilasana": {
        "left_elbow": 175, "right_elbow": 175,
        "left_shoulder": 65, "right_shoulder": 60,
        "left_knee": 85, "right_knee": 85,
        "left_hip": 115, "right_hip": 115
    },
    "Dandasana": {
        "left_elbow": 165, "right_elbow": 170,
        "left_shoulder": 10, "right_shoulder": 10,
        "left_knee": 170, "right_knee": 170,
        "left_hip": 100, "right_hip": 100
    },
    "Dhanurasana": {
        "left_elbow": 165, "right_elbow": 165,
        "left_shoulder": 80, "right_shoulder": 85,
        "left_knee": 105, "right_knee": 105,
        "left_hip": 90, "right_hip": 85
    },
    "Halasana": {
        "left_elbow": 168, "right_elbow": 177,
        "left_shoulder": 86, "right_shoulder": 85,
        "left_knee": 174, "right_knee": 179,
        "left_hip": 38, "right_hip": 43
    },
    
    "Malasana": {
        "left_elbow": 65, "right_elbow": 50,
        "left_shoulder": 20, "right_shoulder": 20,
        "left_knee": 20, "right_knee": 20,
        "left_hip": 30, "right_hip": 30
    },
    "Padmasana": {
        "left_elbow": 165, "right_elbow": 160,
        "left_shoulder": 15, "right_shoulder": 15,
        "left_knee": 30, "right_knee": 21,
        "left_hip": 115, "right_hip": 110
    },
    "Paripurna Navasana": {
        "left_elbow": 164, "right_elbow": 163,
        "left_shoulder": 44, "right_shoulder": 50,
        "left_knee": 175, "right_knee": 175,
        "left_hip": 60, "right_hip": 64
    },



    
    "Phalakasana": {
        "left_elbow": 175, "right_elbow": 178,
        "left_shoulder": 60, "right_shoulder": 60,
        "left_knee": 168, "right_knee": 174,
        "left_hip": 170, "right_hip": 170
    },
    "Setu Bandha Sarvangasana": {
        "left_elbow": 169, "right_elbow": 157,
        "left_shoulder": 65, "right_shoulder": 68,
        "left_knee": 70, "right_knee": 70,
        "left_hip": 140, "right_hip": 142
    },
    "Svarga dvidasana": {
        "left_elbow": 161, "right_elbow": 123,
        "left_shoulder": 5, "right_shoulder": 45,
        "left_knee": 175, "right_knee": 172,
        "left_hip": 167, "right_hip": 49
    },
    "Tadasana Samasthiti": {
        "left_elbow": 180, "right_elbow": 180,
        "left_shoulder": 15, "right_shoulder": 14,
        "left_knee": 180, "right_knee": 180,
        "left_hip": 180, "right_hip": 180
    },
    "Tadasana Urdhva Baddha Hastasana": {
        "left_elbow": 170, "right_elbow": 170,
        "left_shoulder": 180, "right_shoulder": 180,
        "left_knee": 180, "right_knee": 180,
        "left_hip": 180, "right_hip": 180
    },
    "Tadasana Urdhva Hastasana": {
        "left_elbow": 170, "right_elbow": 165,
        "left_shoulder": 170, "right_shoulder": 170,
        "left_knee": 180, "right_knee": 180,
        "left_hip": 180, "right_hip": 180
    },
    "Tittibhasana": {
        "left_elbow": 168, "right_elbow": 178,
        "left_shoulder": 4, "right_shoulder": 17,
        "left_knee": 168, "right_knee": 162,
        "left_hip": 2, "right_hip": 12
    },
    "Urdhva Dandasana": {
        "left_elbow": 64, "right_elbow": 64,
        "left_shoulder": 168, "right_shoulder": 171,
        "left_knee": 171, "right_knee": 165,
        "left_hip": 78, "right_hip": 79
    },
    "Urdhva Dhanurasana": {
        "left_elbow": 161, "right_elbow": 160,
        "left_shoulder": 160, "right_shoulder": 164,
        "left_knee": 125, "right_knee": 128,
        "left_hip": 103, "right_hip": 102
    },
    "Utkata Konasana": {
        "left_elbow": 76, "right_elbow": 82,
        "left_shoulder": 79, "right_shoulder": 90,
        "left_knee": 106, "right_knee": 106,
        "left_hip": 100, "right_hip": 100
    },
    "Utkatasana": {
        "left_elbow": 170, "right_elbow": 169,
        "left_shoulder": 170, "right_shoulder": 172,
        "left_knee": 125, "right_knee": 122,
        "left_hip": 120, "right_hip": 120
    },
    "Uttanasana": {
        "left_elbow": 120, "right_elbow": 110,
        "left_shoulder": 105, "right_shoulder": 98,
        "left_knee": 175, "right_knee": 178,
        "left_hip": 14, "right_hip": 11
    },
    "Marjariasana":  {"left_elbow": 175, "right_elbow": 175, "left_shoulder": 85, "right_shoulder": 78, "left_knee": 85, "right_knee": 85, "left_hip": 95, "right_hip": 95},

    "Vajrasana": {
        "left_elbow": 160, "right_elbow": 145,
        "left_shoulder": 10, "right_shoulder": 10,
        "left_knee": 25, "right_knee": 25,
        "left_hip": 110, "right_hip": 110
    },
    "Utthita Hasta Padasana":  {"left_elbow": 170, "right_elbow": 170, "left_shoulder": 95, "right_shoulder": 95, "left_knee": 178, "right_knee": 175, "left_hip": 145, "right_hip": 149
    },

"Mayurasana":  {"left_elbow": 90, "right_elbow": 105, "left_shoulder": 10, "right_shoulder": 13, "left_knee": 165, "right_knee": 163, "left_hip": 160, "right_hip": 160}
}

# Asymmetric poses

pose_asymmetric = {
    # 1. Ardha Chandrasana (Half Moon)-
    "Ardha Chandrasana-Left":  {"left_elbow": 175, "right_elbow": 175, "left_shoulder": 125,"right_shoulder": 75, "left_knee": 175, "right_knee": 175, "left_hip": 60, "right_hip": 165},

    "Ardha Chandrasana-Right": {"left_elbow": 175, "right_elbow": 175, "left_shoulder": 85, "right_shoulder": 115, "left_knee": 175, "right_knee": 175, "left_hip": 172, "right_hip": 68},

    # 2. Ardha Matsyendrasana (Half Lord of the Fishes)-
    "Ardha Matsyendrasana-Left":  {"left_elbow": 175, "right_elbow": 175, "left_shoulder": 25, "right_shoulder": 35, "left_knee": 70, "right_knee": 30, "left_hip": 55, "right_hip": 85},

    "Ardha Matsyendrasana-Right": {"left_elbow": 175, "right_elbow": 175, "left_shoulder": 35, "right_shoulder": 15, "left_knee": 25, "right_knee": 65, "left_hip": 90, "right_hip": 55},

    # 5. Vrkshasana (Tree Pose)-
    "Vrkshasana-Left":  {"left_elbow": 155, "right_elbow": 155, "left_shoulder": 175, "right_shoulder": 175, "left_knee": 25, "right_knee": 175, "left_hip": 125, "right_hip": 175},

    "Vrkshasana-Right": {"left_elbow": 155, "right_elbow": 157, "left_shoulder": 175, "right_shoulder": 175, "left_knee": 175, "right_knee": 25, "left_hip": 175, "right_hip": 135},

    # 7. Virabhadrasana One-
    "Virabhadrasana One-Left":  {"left_elbow": 175, "right_elbow": 175, "left_shoulder": 175, "right_shoulder": 170, "left_knee": 170, "right_knee": 100, "left_hip": 125, "right_hip": 106},

    "Virabhadrasana One-Right": {"left_elbow": 175, "right_elbow": 175, "left_shoulder": 160, "right_shoulder": 160, "left_knee": 100, "right_knee": 170, "left_hip": 100, "right_hip": 124},

    # 8. Virabhadrasana Two-
    "Virabhadrasana Two-Left":  {"left_elbow": 180, "right_elbow": 180, "left_shoulder": 90, "right_shoulder": 97, "left_knee": 110, "right_knee": 180, "left_hip": 100, "right_hip": 135},

    "Virabhadrasana Two-Right": {"left_elbow": 180, "right_elbow": 180, "left_shoulder": 90, "right_shoulder": 95, "left_knee": 180, "right_knee": 110, "left_hip": 130, "right_hip": 105},

    # 9. Anjaneyasana (Low Lunge) * - right (detection)
    "Anjaneyasana-Left":  {"left_elbow": 155, "right_elbow": 155, "left_shoulder": 157, "right_shoulder": 157, "left_knee": 55, "right_knee": 133, "left_hip": 70, "right_hip": 125},

    "Anjaneyasana-Right": {"left_elbow": 155, "right_elbow": 160, "left_shoulder": 165, "right_shoulder": 165, "left_knee": 145, "right_knee": 65, "left_hip": 120, "right_hip": 70},

    # 10. Gomukhasana-
    "Gomukhasana-Left":  {"left_elbow": 60, "right_elbow": 25, "left_shoulder": 2, "right_shoulder": 170, "left_knee": 105, "right_knee": 85, "left_hip": 65, "right_hip": 180},

    "Gomukhasana-Right": {"left_elbow": 65, "right_elbow": 25, "left_shoulder": 2, "right_shoulder": 170, "left_knee": 104, "right_knee": 63, "left_hip": 175, "right_hip": 25},

    # 11. Kapotasana (Pigeon Pose) * detection
    "Kapotasana-Left":  {"left_elbow": 100, "right_elbow": 100, "left_shoulder": 110, "right_shoulder": 110, "left_knee": 60, "right_knee": 160, "left_hip": 60, "right_hip": 150},

    "Kapotasana-Right": {"left_elbow": 100, "right_elbow": 100, "left_shoulder": 110, "right_shoulder": 110, "left_knee": 160, "right_knee": 60, "left_hip": 150, "right_hip": 60},

    # 13. Natarajasana (Dancer Pose)-
    "Natarajasana-Left":  {"left_elbow": 165, "right_elbow": 165, "left_shoulder": 104, "right_shoulder": 140, "left_knee": 120, "right_knee": 170, "left_hip": 70, "right_hip": 135},

    "Natarajasana-Right": {"left_elbow": 130, "right_elbow": 170, "left_shoulder": 140, "right_shoulder": 90, "left_knee": 175, "right_knee": 115, "left_hip": 125, "right_hip": 85},

    # 14. Parighasana (Gate Pose)-
    "Parighasana-Left":  {"left_elbow": 172, "right_elbow": 165, "left_shoulder": 72, "right_shoulder": 170, "left_knee": 174, "right_knee": 51, "left_hip": 75, "right_hip": 160},

    "Parighasana-Right": {"left_elbow": 145, "right_elbow": 176, "left_shoulder": 155, "right_shoulder": 60, "left_knee": 165, "right_knee": 170, "left_hip": 153, "right_hip": 96},
        
        

    # 15. Parivritta Trikonasana (Revolved Triangle)-
    "Parivritta Trikonasana-Left":  {"left_elbow": 168, "right_elbow": 170, "left_shoulder": 90, "right_shoulder": 120, "left_knee": 175, "right_knee": 175, "left_hip": 85, "right_hip": 143},

    "Parivritta Trikonasana-Right": {"left_elbow": 175, "right_elbow": 175, "left_shoulder": 115, "right_shoulder": 105, "left_knee": 170, "right_knee": 170, "left_hip": 140, "right_hip": 45},

    # 16. Svarga Dvidasana (Bird of Paradise)-
    "Svarga Dvidasana-Left":  {"left_elbow": 150, "right_elbow": 120, "left_shoulder": 2, "right_shoulder": 45, "left_knee": 172, "right_knee": 162, "left_hip": 165, "right_hip": 25},

    "Svarga Dvidasana-Right": {"left_elbow": 83, "right_elbow": 117, "left_shoulder": 34, "right_shoulder": 7, "left_knee": 170, "right_knee": 177, "left_hip": 24, "right_hip": 161},

    # 17. Uttana Shishosana * detection
    "Uttana Shishosana-Left":  {"left_elbow": 170, "right_elbow": 170, "left_shoulder": 145, "right_shoulder": 145, "left_knee": 95, "right_knee": 95, "left_hip": 73, "right_hip": 73},

    "Uttana Shishosana-Right": {"left_elbow": 165, "right_elbow": 165, "left_shoulder": 155, "right_shoulder": 150, "left_knee": 90, "right_knee": 90, "left_hip": 45, "right_hip": 45},

    # 18. Utthita Parsvakonasana-
    "Utthita Parsvakonasana-Left":  {"left_elbow": 175, "right_elbow": 165, "left_shoulder": 60, "right_shoulder": 170, "left_knee": 90, "right_knee": 175, "left_hip": 25, "right_hip": 175},

    "Utthita Parsvakonasana-Right": {"left_elbow": 175, "right_elbow": 170, "left_shoulder": 170, "right_shoulder": 70, "left_knee": 175, "right_knee": 95, "left_hip": 172, "right_hip": 20},

    

    # 20. Utthita Hasta Padangusthasana-
    "Utthita Hasta Padangusthasana-Left":  {"left_elbow": 175, "right_elbow": 175, "left_shoulder": 105, "right_shoulder": 105, "left_knee": 175, "right_knee": 175, "left_hip": 60, "right_hip": 170},

    "Utthita Hasta Padangusthasana-Right": {"left_elbow": 165, "right_elbow": 175, "left_shoulder": 95, "right_shoulder": 100, "left_knee": 175, "right_knee": 179, "left_hip": 170, "right_hip": 60},

    # 21. Utthita Trikonasana * (same as Parivritta Trikonasana - revolved)
    "Utthita Trikonasana-Left":  {"left_elbow": 168, "right_elbow": 170, "left_shoulder": 110, "right_shoulder": 95, "left_knee": 175, "right_knee": 175, "left_hip": 40, "right_hip": 120},

    "Utthita Trikonasana-Right": {"left_elbow": 175, "right_elbow": 175, "left_shoulder": 115, "right_shoulder": 111, "left_knee": 165, "right_knee": 170, "left_hip": 120, "right_hip": 75},

    # 22. Vasisthasana (Side Plank)-
    "Vasisthasana-Left":  {"left_elbow": 175, "right_elbow": 170, "left_shoulder": 80, "right_shoulder": 130, "left_knee": 180, "right_knee": 180, "left_hip": 170, "right_hip": 170},

    "Vasisthasana-Right": {"left_elbow": 170, "right_elbow": 90, "left_shoulder": 170, "right_shoulder": 90, "left_knee": 180, "right_knee": 180, "left_hip": 170, "right_hip": 170},

    # 23. Virabhadrasana Three-
    "Virabhadrasana Three-Left":  {"left_elbow": 165, "right_elbow": 165, "left_shoulder": 160, "right_shoulder": 160, "left_knee": 165, "right_knee": 175, "left_hip": 170, "right_hip": 90},

    "Virabhadrasana Three-Right": {"left_elbow": 165, "right_elbow": 165, "left_shoulder": 165, "right_shoulder": 165, "left_knee": 170, "right_knee": 168, "left_hip": 95, "right_hip": 165},

    # 24. Visvamitrasana-
    "Visvamitrasana-Right":  {"left_elbow": 130, "right_elbow": 177, "left_shoulder": 140, "right_shoulder": 63, "left_knee": 178, "right_knee": 174, "left_hip": 171, "right_hip": 15},

    "Visvamitrasana-Left": {"left_elbow": 174, "right_elbow": 178, "left_shoulder": 94, "right_shoulder": 60, "left_knee": 170, "right_knee": 179, "left_hip": 176, "right_hip": 30},

    # 25. Vrichikasana (Scorpion Pose)-
    "Vrichikasana-Left":  {"left_elbow": 85, "right_elbow": 84, "left_shoulder": 157, "right_shoulder": 152, "left_knee": 60, "right_knee": 60, "left_hip": 136, "right_hip": 133},

    "Vrichikasana-Right": {"left_elbow": 110, "right_elbow": 75, "left_shoulder": 150, "right_shoulder": 135, "left_knee": 95, "right_knee": 90, "left_hip": 105, "right_hip": 110}
}


POSE_FEEDBACK = {
    "Pranamasana":{"left_elbow": "Keep left elbow straight",
        "right_elbow": "Keep right elbow straight",
        "left_shoulder": "Relax left shoulder down",
        "right_shoulder": "Relax right shoulder down",
        "left_knee": "Engage left knee firmly",
        "right_knee": "Engage right knee firmly",
        "left_hip": "Balance left hip evenly",
        "right_hip": "Balance right hip evenly"},

        "Padahastasana":{
           "left_elbow": "Keep left elbow straight",
        "right_elbow": "Keep right elbow straight",
        "left_shoulder": "Relax left shoulder down",
        "right_shoulder": "Relax right shoulder down",
        "left_knee": "Engage left knee firmly",
        "right_knee": "Engage right knee firmly",
        "left_hip": "Balance left hip evenly",
        "right_hip": "Balance right hip evenly" 
        },

        "Ashtanaga Namaskar":{
        "left_elbow": "Keep left elbow straight",
        "right_elbow": "Keep right elbow straight",
        "left_shoulder": "Open left shoulder outward",
        "right_shoulder": "Open right shoulder outward",
        "left_knee": "Straighten left leg fully",
        "right_knee": "Straighten right leg fully",
        "left_hip": "Lift left hip high",
        "right_hip": "Lift right hip high"
        },
        "Ashwa Sanchalanasana":{
        "left_elbow": "Keep left elbow straight",
        "right_elbow": "Keep right elbow straight",
        "left_shoulder": "Open left shoulder outward",
        "right_shoulder": "Open right shoulder outward",
        "left_knee": "Straighten left leg fully",
        "right_knee": "Straighten right leg fully",
        "left_hip": "Lift left hip high",
        "right_hip": "Lift right hip high"
        },
         "Chaturanga Dandasana":{ "left_elbow": "Keep left elbow relaxed",
        "right_elbow": "Keep right elbow relaxed",
        "left_shoulder": "Keep left shoulder relaxed",
        "right_shoulder": "Keep right shoulder relaxed",
        "left_knee": "Bring left knee outward",
        "right_knee": "Bring right knee outward",
        "left_hip": "Open left hip",
        "right_hip": "Open right hip"},

    "Tadasana Samasthiti": {
        "left_elbow": "Keep left elbow straight",
        "right_elbow": "Keep right elbow straight",
        "left_shoulder": "Relax left shoulder down",
        "right_shoulder": "Relax right shoulder down",
        "left_knee": "Engage left knee firmly",
        "right_knee": "Engage right knee firmly",
        "left_hip": "Balance left hip evenly",
        "right_hip": "Balance right hip evenly"
    },

    "Tadasana Urdhva Hastasana": {
        "left_elbow": "Straighten left elbow fully",
        "right_elbow": "Straighten right elbow fully",
        "left_shoulder": "Lift left shoulder upwards",
        "right_shoulder": "Lift right shoulder upwards",
        "left_knee": "Engage left knee firmly",
        "right_knee": "Engage right knee firmly",
        "left_hip": "Ground left hip firmly",
        "right_hip": "Ground right hip firmly"
    },
   
    "Tadasana Urdhva Baddha Hastasana": {
        "left_elbow": "Extend left elbow strongly",
        "right_elbow": "Extend right elbow strongly",
        "left_shoulder": "Open left shoulder fully",
        "right_shoulder": "Open right shoulder fully",
        "left_knee": "Straighten left knee firmly",
        "right_knee": "Straighten right knee firmly",
        "left_hip": "Anchor left hip evenly",
        "right_hip": "Anchor right hip evenly"
    },
    "Adho Mukha Svanasana":{
        "left_elbow": "Keep left elbow straight",
        "right_elbow": "Keep right elbow straight",
        "left_shoulder": "Open left shoulder outward",
        "right_shoulder": "Open right shoulder outward",
        "left_knee": "Straighten left leg fully",
        "right_knee": "Straighten right leg fully",
        "left_hip": "Lift left hip high",
        "right_hip": "Lift right hip high"
    },
    
    "Ananda balasana": {
        "left_elbow": "Keep left elbow relaxed",
        "right_elbow": "Keep right elbow relaxed",
        "left_shoulder": "Keep left shoulder relaxed",
        "right_shoulder": "Keep right shoulder relaxed",
        "left_knee": "Draw left knee toward chest",
        "right_knee": "Draw right knee toward chest",
        "left_hip": "Open left hip gently",
        "right_hip": "Open right hip gently"
    },
    "Ardha Chakrasana": {
        "left_elbow": "Keep left elbow relaxed",
        "right_elbow": "Keep right elbow relaxed",
        "left_shoulder": "Lift left shoulder up",
        "right_shoulder": "Lift right shoulder up",
        "left_knee": "Straighten left knee",
        "right_knee": "Straighten right knee",
        "left_hip": "Push left hip forward",
        "right_hip": "Push right hip forward"
    },
    "Ardha Uttasana": {
        "left_elbow": "Keep left elbow relaxed",
        "right_elbow": "Keep right elbow relaxed",
        "left_shoulder": "Extend left shoulder forward",
        "right_shoulder": "Extend right shoulder forward",
        "left_knee": "Keep left knee straight",
        "right_knee": "Keep right knee straight",
        "left_hip": "Hinge left hip back",
        "right_hip": "Hinge right hip back"
    },
    "Ardha Chandrasana": {
        "left_elbow": "Extend left elbow fully",
        "right_elbow": "Extend right elbow fully",
        "left_shoulder": "Open left shoulder outward",
        "right_shoulder": "Open right shoulder outward",
        "left_knee": "Engage left knee firmly",
        "right_knee": "Lift right knee upward",
        "left_hip": "Stabilize left hip evenly",
        "right_hip": "Lift right hip gently"
    },
    "Ardha Matsyendrasana": {
        "left_elbow": "Keep left elbow slightly bent",
        "right_elbow": "Keep right elbow slightly bent",
        "left_shoulder": "Twist left shoulder gently",
        "right_shoulder": "Twist right shoulder gently",
        "left_knee": "Keep left knee grounded",
        "right_knee": "Cross right knee firmly",
        "left_hip": "Anchor left hip evenly",
        "right_hip": "Rotate right hip slightly"
    },
    "Baddha Konasana": {
        "left_elbow": "Keep left elbow relaxed",
        "right_elbow": "Keep right elbow relaxed",
        "left_shoulder": "Keep left shoulder relaxed",
        "right_shoulder": "Keep right shoulder relaxed",
        "left_knee": "Bring left knee outward",
        "right_knee": "Bring right knee outward",
        "left_hip": "Open left hip",
        "right_hip": "Open right hip"
    },
    "Balasana": {
        "left_elbow": "Keep left elbow relaxed",
        "right_elbow": "Keep right elbow relaxed",
        "left_shoulder": "Keep left shoulder relaxed",
        "right_shoulder": "Keep right shoulder relaxed",
        "left_knee": "Fold left knee inward",
        "right_knee": "Fold right knee inward",
        "left_hip": "Relax left hip down",
        "right_hip": "Relax right hip down"
    },
    "Bitilasana": {
        "left_elbow": "Keep left elbow relaxed",
        "right_elbow": "Keep right elbow relaxed",
        "left_shoulder": "Drop left shoulder down",
        "right_shoulder": "Drop right shoulder down",
        "left_knee": "Keep left knee relaxed",
        "right_knee": "Keep right knee relaxed",
        "left_hip": "Keep left hip neutral",
        "right_hip": "Keep right hip neutral"
    },
    "Dandasana": {
        "left_elbow": "Keep left elbow relaxed",
        "right_elbow": "Keep right elbow relaxed",
        "left_shoulder": "Keep left shoulder relaxed",
        "right_shoulder": "Keep right shoulder relaxed",
        "left_knee": "Straighten left knee",
        "right_knee": "Straighten right knee",
        "left_hip": "Engage left hip",
        "right_hip": "Engage right hip"
    },
    "Dhanurasana": {
        "left_elbow": "Pull left elbow backward",
        "right_elbow": "Pull right elbow backward",
        "left_shoulder": "Open left shoulder upward",
        "right_shoulder": "Open right shoulder upward",
        "left_knee": "Lift left knee upward",
        "right_knee": "Lift right knee upward",
        "left_hip": "Push left hip downward",
        "right_hip": "Push right hip downward"
    },
    "Malasana": {
        "left_elbow": "Press left elbow inward",
        "right_elbow": "Press right elbow inward",
        "left_shoulder": "Relax left shoulder down",
        "right_shoulder": "Relax right shoulder down",
        "left_knee": "Keep left knee wide",
        "right_knee": "Keep right knee wide",
        "left_hip": "Sink left hip evenly",
        "right_hip": "Sink right hip evenly"
    },
    "Marjariasana": {
         "left_elbow": "Keep left elbow relaxed",
        "right_elbow": "Keep right elbow relaxed",
        "left_shoulder": "Relax left shoulder",
        "right_shoulder": "Relax right shoulder",
        "left_knee": "Keep left knee neutral",
        "right_knee": "Keep right knee neutral",
        "left_hip": "Keep left hip neutral",
        "right_hip": "Keep right hip neutral"
    },
    "Padmasana": {
        "left_elbow": "Relax left elbow gently",
        "right_elbow": "Relax right elbow gently",
        "left_shoulder": "Open left shoulder slightly",
        "right_shoulder": "Open right shoulder slightly",
        "left_knee": "Fold left knee fully",
        "right_knee": "Fold right knee fully",
        "left_hip": "Anchor left hip evenly",
        "right_hip": "Anchor right hip evenly"
    },
    "Utkatasana": {
        "left_elbow": "Extend left elbow forward",
        "right_elbow": "Extend right elbow forward",
        "left_shoulder": "Lift left shoulder upward",
        "right_shoulder": "Lift right shoulder upward",
        "left_knee": "Bend left knee deeply",
        "right_knee": "Bend right knee deeply",
        "left_hip": "Push left hip back",
        "right_hip": "Push right hip back"
    },
    "Vrkshasana": {
        "left_elbow": "Keep left elbow relaxed",
        "right_elbow": "Keep right elbow relaxed",
        "left_shoulder": "Open left shoulder outward",
        "right_shoulder": "Open right shoulder outward",
        "left_knee": "Anchor left knee firmly",
        "right_knee": "Lift right knee to thigh",
        "left_hip": "Stabilize left hip evenly",
        "right_hip": "Balance right hip gently"
    },
    "Vajrasana": {
       "left_elbow": "Keep left elbow relaxed",
        "right_elbow": "Keep right elbow relaxed",
        "left_shoulder": "Keep left shoulder relaxed",
        "right_shoulder": "Keep right shoulder relaxed",
        "left_knee": "Sit on left knee",
        "right_knee": "Sit on right knee",
        "left_hip": "Anchor left hip",
        "right_hip": "Anchor right hip"
    },
    "Virabhadrasana One": {
        "left_elbow": "Keep left elbow relaxed",
        "right_elbow": "Keep right elbow relaxed",
        "left_shoulder": "Lift left arm up",
        "right_shoulder": "Lift right arm up",
        "left_knee": "Bend left knee forward",
        "right_knee": "Keep right leg straight",
        "left_hip": "Rotate left hip forward",
        "right_hip": "Rotate right hip back"
    },
    "Virabhadrasana Two": {
        "left_elbow": "Keep left elbow relaxed",
        "right_elbow": "Keep right elbow relaxed",
        "left_shoulder": "Stretch left arm sideways",
        "right_shoulder": "Stretch right arm sideways",
        "left_knee": "Bend left knee forward",
        "right_knee": "Keep right leg straight",
        "left_hip": "Open left hip",
        "right_hip": "Open right hip"
    },
    "Anantasana": {
    "left_elbow": "Bend left elbow deeply",
    "right_elbow": "Straighten right elbow fully",
    "left_shoulder": "Bend left shoulder slightly",
    "right_shoulder": "Bend right shoulder deeply",
    "left_knee": "Straighten left knee fully",
    "right_knee": "Straighten right knee fully",
    "left_hip": "Straighten left hip fully",
    "right_hip": "Fold right hip inward"
},
"Anjaneyasana": {
    "left_elbow": "Bend left elbow slightly",
    "right_elbow": "Bend right elbow slightly",
    "left_shoulder": "Bend left shoulder slightly",
    "right_shoulder": "Bend right shoulder slightly",
    "left_knee": "Bend left knee deeply",
    "right_knee": "Bend right knee slightly",
    "left_hip": "Bend left hip deeply",
    "right_hip": "Bend right hip slightly"
},
"Bhujangasana": {
    "left_elbow": "Bend left elbow slightly",
    "right_elbow": "Bend right elbow slightly",
    "left_shoulder": "Fold left shoulder inward",
    "right_shoulder": "Fold right shoulder inward",
    "left_knee": "Straighten left knee fully",
    "right_knee": "Straighten right knee fully",
    "left_hip": "Bend left hip deeply",
    "right_hip": "Bend right hip deeply"
},
"Gomukhasana": {
    "left_elbow": "Bend left elbow deeply",
    "right_elbow": "Bend right elbow deeply",
    "left_shoulder": "Fold left shoulder inward",
    "right_shoulder": "Straighten right shoulder fully",
    "left_knee": "Bend left knee deeply",
    "right_knee": "Bend right knee deeply",
    "left_hip": "Straighten left hip fully",
    "right_hip": "Straighten right hip fully"
},
"Halasana": {
    "left_elbow": "Bend left elbow slightly",
    "right_elbow": "Straighten right elbow fully",
    "left_shoulder": "Bend left shoulder deeply",
    "right_shoulder": "Bend right shoulder deeply",
    "left_knee": "Straighten left knee fully",
    "right_knee": "Straighten right knee fully",
    "left_hip": "Fold left hip inward",
    "right_hip": "Fold right hip inward"
},
"Kapotasana": {
    "left_elbow": "Bend left elbow deeply",
    "right_elbow": "Bend right elbow deeply",
    "left_shoulder": "Straighten left shoulder fully",
    "right_shoulder": "Straighten right shoulder fully",
    "left_knee": "Bend left knee deeply",
    "right_knee": "Bend right knee deeply",
    "left_hip": "Bend left hip deeply",
    "right_hip": "Bend right hip deeply"
},
"Mayurasana": {
    "left_elbow": "Bend left elbow deeply",
    "right_elbow": "Bend right elbow deeply",
    "left_shoulder": "Fold left shoulder inward",
    "right_shoulder": "Fold right shoulder inward",
    "left_knee": "Straighten left knee fully",
    "right_knee": "Straighten right knee fully",
    "left_hip": "Straighten left hip fully",
    "right_hip": "Straighten right hip fully"
},
"Natarajasana": {
    "left_elbow": "Bend left elbow slightly",
    "right_elbow": "Straighten right elbow fully",
    "left_shoulder": "Bend left shoulder slightly",
    "right_shoulder": "Bend right shoulder deeply",
    "left_knee": "Straighten left knee fully",
    "right_knee": "Bend right knee deeply",
    "left_hip": "Bend left hip deeply",
    "right_hip": "Bend right hip deeply"
},
"Parighasana": {
    "left_elbow": "Straighten left elbow fully",
    "right_elbow": "Bend right elbow slightly",
    "left_shoulder": "Bend left shoulder slightly",
    "right_shoulder": "Bend right shoulder deeply",
    "left_knee": "Bend left knee deeply",
    "right_knee": "Straighten right knee fully",
    "left_hip": "Bend left hip slightly",
    "right_hip": "Bend right hip deeply"
},
"Paripurna Navasana": {
    "left_elbow": "Bend left elbow slightly",
    "right_elbow": "Bend right elbow slightly",
    "left_shoulder": "Fold left shoulder inward",
    "right_shoulder": "Fold right shoulder inward",
    "left_knee": "Straighten left knee fully",
    "right_knee": "Straighten right knee fully",
    "left_hip": "Fold left hip inward",
    "right_hip": "Fold right hip inward"
},
"Phalakasana": {
    "left_elbow": "Straighten left elbow fully",
    "right_elbow": "Straighten right elbow fully",
    "left_shoulder": "Bend left shoulder deeply",
    "right_shoulder": "Bend right shoulder deeply",
    "left_knee": "Straighten left knee fully",
    "right_knee": "Straighten right knee fully",
    "left_hip": "Bend left hip slightly",
    "right_hip": "Straighten right hip fully"
},
"Parivritta Trikonasana": {
    "left_elbow": "Fold left elbow inward",
    "right_elbow": "Fold right elbow inward",
    "left_shoulder": "Fold left shoulder inward",
    "right_shoulder": "Fold right shoulder inward",
    "left_knee": "Fold left knee inward",
    "right_knee": "Fold right knee inward",
    "left_hip": "Fold left hip inward",
    "right_hip": "Fold right hip inward"
},
"Setu Bandha Sarvangasana": {
    "left_elbow": "Bend left elbow slightly",
    "right_elbow": "Bend right elbow slightly",
    "left_shoulder": "Bend left shoulder deeply",
    "right_shoulder": "Bend right shoulder deeply",
    "left_knee": "Bend left knee deeply",
    "right_knee": "Bend right knee deeply",
    "left_hip": "Straighten left hip fully",
    "right_hip": "Straighten right hip fully"
},
"Svarga Dvidasana": {
    "left_elbow": "Bend left elbow slightly",
    "right_elbow": "Bend right elbow deeply",
    "left_shoulder": "Fold left shoulder inward",
    "right_shoulder": "Fold right shoulder inward",
    "left_knee": "Straighten left knee fully",
    "right_knee": "Straighten right knee fully",
    "left_hip": "Straighten left hip fully",
    "right_hip": "Bend right hip deeply"
},
"Tittibhasana": {
    "left_elbow": "Bend left elbow slightly",
    "right_elbow": "Bend right elbow slightly",
    "left_shoulder": "Bend left shoulder deeply",
    "right_shoulder": "Bend right shoulder deeply",
    "left_knee": "Bend left knee slightly",
    "right_knee": "Bend right knee slightly",
    "left_hip": "Fold left hip inward",
    "right_hip": "Fold right hip inward"
},
"Urdhva Dandasana": {
    "left_elbow": "Bend left elbow deeply",
    "right_elbow": "Bend right elbow deeply",
    "left_shoulder": "Straighten left shoulder fully",
    "right_shoulder": "Straighten right shoulder fully",
    "left_knee": "Straighten left knee fully",
    "right_knee": "Straighten right knee fully",
    "left_hip": "Bend left hip deeply",
    "right_hip": "Bend right hip deeply"
},
"Urdhva Dhanurasana": {
    "left_elbow": "Bend left elbow slightly",
    "right_elbow": "Bend right elbow slightly",
    "left_shoulder": "Bend left shoulder slightly",
    "right_shoulder": "Bend right shoulder slightly",
    "left_knee": "Bend left knee slightly",
    "right_knee": "Bend right knee slightly",
    "left_hip": "Bend left hip deeply",
    "right_hip": "Bend right hip deeply"
},
"Utkata Konasana": {
    "left_elbow": "Bend left elbow deeply",
    "right_elbow": "Bend right elbow deeply",
    "left_shoulder": "Bend left shoulder deeply",
    "right_shoulder": "Bend right shoulder deeply",
    "left_knee": "Bend left knee slightly",
    "right_knee": "Bend right knee slightly",
    "left_hip": "Bend left hip deeply",
    "right_hip": "Bend right hip deeply"
},
"Uttana shishosana": {
    "left_elbow": "Bend left elbow slightly",
    "right_elbow": "Bend right elbow slightly",
    "left_shoulder": "Bend left shoulder slightly",
    "right_shoulder": "Bend right shoulder slightly",
    "left_knee": "Bend left knee deeply",
    "right_knee": "Bend right knee deeply",
    "left_hip": "Fold left hip inward",
    "right_hip": "Fold right hip inward"
},
"Uttanasana": {
    "left_elbow": "Bend left elbow deeply",
    "right_elbow": "Bend right elbow deeply",
    "left_shoulder": "Bend left shoulder deeply",
    "right_shoulder": "Bend right shoulder deeply",
    "left_knee": "Straighten left knee fully",
    "right_knee": "Straighten right knee fully",
    "left_hip": "Fold left hip inward",
    "right_hip": "Fold right hip inward"
},
"Utthita Hasta Padangusthasana": {
    "left_elbow": "Bend left elbow deeply",
    "right_elbow": "Straighten right elbow fully",
    "left_shoulder": "Bend left shoulder deeply",
    "right_shoulder": "Bend right shoulder slightly",
    "left_knee": "Straighten left knee fully",
    "right_knee": "Straighten right knee fully",
    "left_hip": "Straighten left hip fully",
    "right_hip": "Bend right hip deeply"
},
"Utthita Hasta Padasana": {
    "left_elbow": "Straighten left elbow fully",
    "right_elbow": "Straighten right elbow fully",
    "left_shoulder": "Bend left shoulder deeply",
    "right_shoulder": "Bend right shoulder deeply",
    "left_knee": "Straighten left knee fully",
    "right_knee": "Straighten right knee fully",
    "left_hip": "Bend left hip slightly",
    "right_hip": "Bend right hip slightly"
},
"Utthita Parsvakonasana": {
    "left_elbow": "Straighten left elbow fully",
    "right_elbow": "Bend right elbow slightly",
    "left_shoulder": "Bend left shoulder deeply",
    "right_shoulder": "Straighten right shoulder fully",
    "left_knee": "Bend left knee deeply",
    "right_knee": "Straighten right knee fully",
    "left_hip": "Fold left hip inward",
    "right_hip": "Straighten right hip fully"
},
"Utthita Trikonasana": {
    "left_elbow": "Straighten left elbow fully",
    "right_elbow": "Straighten right elbow fully",
    "left_shoulder": "Bend left shoulder deeply",
    "right_shoulder": "Bend right shoulder deeply",
    "left_knee": "Straighten left knee fully",
    "right_knee": "Straighten right knee fully",
    "left_hip": "Fold left hip inward",
    "right_hip": "Bend right hip slightly"
},
"Vasisthasana": {
    "left_elbow": "Straighten left elbow fully",
    "right_elbow": "Straighten right elbow fully",
    "left_shoulder": "Bend left shoulder slightly",
    "right_shoulder": "Bend right shoulder deeply",
    "left_knee": "Straighten left knee fully",
    "right_knee": "Straighten right knee fully",
    "left_hip": "Straighten left hip fully",
    "right_hip": "Straighten right hip fully"
},
"Virabhadrasana Three": {
    "left_elbow": "Straighten left elbow fully",
    "right_elbow": "Straighten right elbow fully",
    "left_shoulder": "Straighten left shoulder fully",
    "right_shoulder": "Straighten right shoulder fully",
    "left_knee": "Straighten left knee fully",
    "right_knee": "Straighten right knee fully",
    "left_hip": "Bend left hip deeply",
    "right_hip": "Bend right hip slightly"
},
"Visvamitrasana": {
    "left_elbow": "Bend left elbow slightly",
    "right_elbow": "Straighten right elbow fully",
    "left_shoulder": "Bend left shoulder slightly",
    "right_shoulder": "Bend right shoulder deeply",
    "left_knee": "Straighten left knee fully",
    "right_knee": "Straighten right knee fully",
    "left_hip": "Straighten left hip fully",
    "right_hip": "Fold right hip inward"
},
"Vrichikasana": {
    "left_elbow": "Bend left elbow deeply",
    "right_elbow": "Bend right elbow deeply",
    "left_shoulder": "Bend left shoulder deeply",
    "right_shoulder": "Bend right shoulder deeply",
    "left_knee": "Bend left knee slightly",
    "right_knee": "Bend right knee slightly",
    "left_hip": "Bend left hip deeply",
    "right_hip": "Bend right hip deeply"
},


}
pose_side_rules = {
    "ardhachandrasana": [("left_hip","right_hip"), ("left_shoulder","right_shoulder")],
    "ardhamatsyendrasana": [("left_hip","right_hip"), ("left_shoulder","right_shoulder")],
    "baddhakonasana": [("left_knee","right_knee"), ("left_hip","right_hip")],
    "vrkshasana": [("left_knee","right_knee"), ("left_hip","right_hip")],
    "anjaneyasana": [("left_knee","right_knee"), ("left_hip","right_hip")],
    "gomukhasana": [("left_hip","right_hip"),("left_knee","right_knee"),("left_elbow","right_elbow")],
    "kapotasana": [("left_hip","right_hip"), ("left_knee","right_knee")],
    "mayurasana": [("left_elbow","right_elbow"), ("left_shoulder","right_shoulder")],
    "natarajasana": [("left_hip","right_hip"), ("left_shoulder","right_shoulder")],
    "parighasana": [("left_shoulder","right_shoulder"), ("left_hip","right_hip")],
    "parivrittatrikonasana": [("left_shoulder","right_shoulder"), ("left_hip","right_hip")],
    "svargadvidasana": [("left_hip","right_hip"), ("left_shoulder","right_shoulder")],
    "uttanashishosana": [("left_shoulder","right_shoulder")],  # mostly shoulder opening
    "utthitahastapadangusthasana": [("left_knee","right_knee"), ("left_hip","right_hip")],
    "utthitahastapadasana": [("left_knee","right_knee"), ("left_hip","right_hip")],
    "utthitaparsvakonasana": [("left_knee","right_knee"), ("left_shoulder","right_shoulder")],
    "utthitatrikonasana": [("left_shoulder","right_shoulder"), ("left_hip","right_hip")],
    "vasisthasana": [("left_shoulder","right_shoulder"), ("left_hip","right_hip")],
    "visvamitrasana": [("left_hip","right_hip"), ("left_shoulder","right_shoulder")],
    "virabhadrasana-three":[("left_knee","right_knee"),("left_hip","right_hip"), ("left_shoulder","right_shoulder")],
    "vrichikasana": [("left_shoulder","right_shoulder"), ("left_hip","right_hip"),("left_knee","right_knee"),("left_elbow","right_elbow")],
}

def infer_side(pose_name, angles, joint_names, tolerance=None):
    """
    Return pose_name (unchanged) or pose_name + '-Left'/'-Right' based on joint votes.
    - angles: list/array aligned with joint_names
    - joint_names: list of strings
    - tolerance: minimum angle diff to count as evidence
    """
    if tolerance is None:
        tolerance = max(10, min(25, np.std(angles)))
    # quick check if model already provided side
    lname = pose_name.lower()
    if lname.endswith("-left") or lname.endswith("_left") or " left" in lname:
        return pose_name if pose_name.endswith("-Left") else pose_name + "-Left"
    if lname.endswith("-right") or lname.endswith("_right") or " right" in lname:
        return pose_name if pose_name.endswith("-Right") else pose_name + "-Right"

    # normalize
    def norm(s): return s.lower().replace(" ", "").replace("-", "").replace("_", "")

    npose = norm(pose_name)
    left_key, right_key = None, None
    for key in pose_asymmetric:
        if norm(key).startswith(npose):
            if key.endswith("-Left"): 
                left_key = key
            elif key.endswith("-Right"): 
                right_key = key

    if not left_key or not right_key:
        return pose_name
    

    # helper to get angle
    def get_angle(j):
        try:
            return angles[joint_names.index(j)]
        except ValueError:
            return None

    left_votes = right_votes = 0
    family_key = npose
    if family_key in pose_side_rules:
        for left_joint, right_joint in pose_side_rules[family_key]:
            l_ang = get_angle(left_joint)
            r_ang = get_angle(right_joint)
            if l_ang is None or r_ang is None:
                continue
            if l_ang < r_ang - tolerance:
                left_votes += 1
            elif r_ang < l_ang - tolerance:
                right_votes += 1

    if left_votes > right_votes:
        print(f"[DEBUG] Pose: {pose_name}, Side = Left ({left_votes} vs {right_votes})")
        return pose_name + "-Left"
    elif right_votes > left_votes:
        print(f"[DEBUG] Pose: {pose_name}, Side = Right ({right_votes} vs {left_votes})")
        return pose_name + "-Right"
   
    def total_error(template):
        err, count = 0, 0
        for joint, ideal in template.items():
            ang = get_angle(joint)
            if ang is not None:
                err += abs(ang - ideal)
                count += 1
        return err / count if count > 0 else float("inf")

    left_err = total_error(pose_asymmetric[left_key])
    right_err = total_error(pose_asymmetric[right_key])

    base_name = pose_name.split("-")[0]  # remove suffix if any
    if left_err + tolerance < right_err:
        print(f"[DEBUG] Pose: {pose_name}, Side = Left (err {left_err:.2f} vs {right_err:.2f})")
        return base_name + "-Left"
    elif right_err + tolerance < left_err:
        print(f"[DEBUG] Pose: {pose_name}, Side = Right (err {right_err:.2f} vs {left_err:.2f})")
        return base_name + "-Right"
    else:
        print(f"[DEBUG] Pose: {pose_name}, Side = Undecided (err {left_err:.2f} vs {right_err:.2f})")
        return base_name




# Global state to track stability
pose_state = {
    "last_feedback": None,
    "last_corrections": None,
    "last_update_time": time.time()
}

def check_pose(pose_name, angles, joint_names, tolerance=15, hold_time=4):
    
    global pose_state
    maybe_side = None
    if pose_name == "No Pose Detected":
        return [], ["No Pose Detected"]
    # corrections, feedback = {}, []
    # joint_feedback = {}
    pose_ideal = POSE_SYMMETRIC.get(pose_name)
    if pose_ideal is None:
        # try to infer side for asymmetric families
        maybe_side = infer_side(pose_name, angles, joint_names, tolerance=max(10, tolerance))
        print(f"[DEBUG] Inferred side inside check_pose: {maybe_side}")
        pose_ideal = pose_asymmetric.get(maybe_side)
        if pose_ideal is None:
            # If not in asymmetric dict, try the original name too (in case model already had suffix)
            pose_ideal = pose_asymmetric.get(pose_name)
    # Fallback if pose is unknown
    if not pose_ideal:
        feedback = [f"{pose_name} not defined"]
        corrections = {joint: "gray" for joint in joint_names}
        return corrections, feedback


    # Step 1: calculate current feedback
    corrections, feedback = {}, []
    joint_feedback = {}
    for i, joint in enumerate(joint_names):
        print(f"[DEBUG] {joint}: {angles[i]:.2f}°")
        if joint in pose_ideal:
            diff = abs(angles[i] - pose_ideal[joint])
            if diff > tolerance:
                corrections[joint] = "red"
                # use per-joint prewritten feedback if available (you said you have POSE_FEEDBACK)
                if 'POSE_FEEDBACK' in globals() and pose_name in globals().get('POSE_FEEDBACK', {}) and joint in POSE_FEEDBACK[pose_name]:
                    joint_feedback[joint] = POSE_FEEDBACK[pose_name][joint]
                elif 'POSE_FEEDBACK' in globals() and maybe_side in globals().get('POSE_FEEDBACK', {}) and joint in POSE_FEEDBACK[maybe_side]:
                    joint_feedback[joint] = POSE_FEEDBACK[maybe_side][joint]
                else:
                    joint_feedback[joint] = f"Adjust {joint} → target {pose_ideal[joint]:.0f}°"
            else:
                corrections[joint] = "green"
        else:
            corrections[joint] = "gray"
        
    symmetric_pairs = [("left_elbow", "right_elbow"),
                       ("left_shoulder", "right_shoulder"),
                       ("left_knee", "right_knee"),
                       ("left_hip", "right_hip")]

    used_joints = set()
    for left, right in symmetric_pairs:
        left_msg = joint_feedback.get(left)
        right_msg = joint_feedback.get(right)

        if left_msg:
            feedback.append(left_msg)
            used_joints.add(left)
        if right_msg:
            feedback.append(right_msg)
            used_joints.add(right)

              
            

    # Add remaining single joint feedback
    for joint, msg in joint_feedback.items():
        if joint not in used_joints:
            feedback.append(msg)

    if not feedback:
        feedback = ["Perfect Pose"]


    current_time = time.time()
    if feedback != pose_state.get("last_feedback"):
        pose_state["last_feedback"] = feedback
        pose_state["last_corrections"] = corrections
        pose_state["last_update_time"] = current_time
        speak_feedback(feedback)

    # Step 2: compare with last feedback
    
    else:
        if current_time - pose_state.get("last_update_time", 0) >= hold_time:
            pose_state["last_update_time"] = current_time

    return pose_state["last_corrections"], pose_state["last_feedback"]
