const express = require("express");
const router = express.Router();
const User = require("../models/User");
const jwt = require("jsonwebtoken");

// Middleware to verify JWT
const verifyToken = (req, res, next) => {
  const authHeader = req.headers.authorization;
  if (!authHeader) return res.status(401).json({ message: "No token provided" });

  const token = authHeader.split(" ")[1];
  jwt.verify(token, process.env.JWT_SECRET, (err, decoded) => {
    if (err) return res.status(401).json({ message: "Invalid token" });

    // Make sure correct userId is always set from token
    req.userId = decoded.id;
    next();
  });
};

// GET Personalized Wellness
router.get("/", verifyToken, async (req, res) => {
  try {
    // Always fetch the correct logged-in user
    const user = await User.findById(req.userId).lean();
    if (!user) return res.status(404).json({ message: "User not found" });

    const { age, weight, height, gender, level, disease } = user.wellness || {};
    let tips = [];

    // --- BMI-based ---
    if (weight && height) {
      const w = Number(weight);
      const h = Number(height) / 100;
      const bmi = w / (h * h);
      if (bmi >= 30) {
        tips.push("You are obese. Practice Adho Mukha Svanasana, Balasana, Bitilasana, Ananda Balasana, Tadasana Samasthiti, Vajrasana, and Uttana Shishosana to improve flexibility, circulation, and joint health.");
      }
      else if (bmi >= 25) {
        tips.push("You are overweight. Practice Anantasana, Ardha Matsyendrasana, Bhujangasana, Dhanurasana, Marjariasana, Setu Bandha Sarvangasana, Virabhadrasana I & II, Utthita Trikonasana to strengthen muscles, improve balance, and enhance stamina.");
      }
      else if (bmi < 18.5) {
        tips.push("You are underweight. Practice Adho Mukha Svanasana, Phalakasana, Bitilasana, Setu Bandha Sarvangasana, Vrkshasana, Padmasana, Natarajasana to strengthen muscles, core, and overall endurance.");
      }
      else {
        tips.push("Your BMI is healthy. Maintain flexibility, strength, and balance with Tadasana Urdhva Hastasana, Virabhadrasana I, Utthita Trikonasana, Vrkshasana, Utkatasana, Parivrtta Trikonasana, and Padmasana.");
      }
    }

    // --- Disease-specific ---
    if (disease) {
      switch (disease) {
        case "Diabetes":
          tips.push("For diabetes, practice Bhujangasana, Setu Bandha Sarvangasana, Virabhadrasana I, and Tadasana to improve circulation and support blood sugar regulation.");
          break;
        case "Hypertension":
          tips.push("For hypertension, practice Balasana, Uttanasana, Marjariasana, and Vrkshasana to reduce stress and control blood pressure.");
          break;
        case "Asthma":
          tips.push("For asthma, practice Bhujangasana, Setu Bandha Sarvangasana, Virabhadrasana II, and Utthita Trikonasana to open the chest and improve breathing.");
          break;
        case "Thyroid":
          tips.push("For thyroid, practice Halasana, Setu Bandha Sarvangasana, Marjariasana, and Sarvangasana (if available) to stimulate hormone balance.");
          break;
        case "Back Pain":
          tips.push("For back pain, practice Bhujangasana, Balasana, Setu Bandha Sarvangasana, and Marjariasana to strengthen the spine and relieve tension.");
          break;
        case "Arthritis":
          tips.push("For arthritis, practice Tadasana, Utthita Trikonasana, Vrkshasana, and Utkata Konasana to gently improve joint mobility.");
          break;
        case "Obesity":
          tips.push("For obesity, practice Utkatasana, Virabhadrasana I, Phalakasana, and Adho Mukha Svanasana to support weight loss, stamina, and overall strength.");
          break;
        case "Mental Health Issues":
          tips.push("For mental health, practice Balasana, Vrkshasana, Virabhadrasana II, and Marjariasana to reduce stress and improve focus.");
          break;
        case "Acidity":
          tips.push("For acidity, practice Setu Bandha Sarvangasana, Bhujangasana, Marjariasana, and Balasana to aid digestion and provide comfort.");
          break;
        case "PCOD":
          tips.push("For PCOD, practice Virabhadrasana II, Utthita Trikonasana, Setu Bandha Sarvangasana, and Utkata Konasana to support hormonal health and circulation.");
          break;
        case "Heart Disease":
          tips.push("For heart health, practice Balasana, Uttanasana, Tadasana, and Vrkshasana to calm the nervous system and improve circulation.");
          break;
        case "Other":
          tips.push("For other conditions, practice gentle poses like Marjariasana, Vrkshasana, Virabhadrasana I, and Balasana to improve overall wellness.");
          break;
        default:
          tips.push("Gentle yoga and breathing exercises support your condition.");
      }
    }

    // --- Age-based ---
    if (age !== undefined && age !== null) {
      if (age > 50) {
        tips.push("Above 50, practice Utkatasana, Setu Bandha Sarvangasana, and Vajrasana to improve flexibility, strengthen muscles, and stay joint-friendly.");
      }
      else if (age >= 18) {
        tips.push("As an adult, practice Virabhadrasana I & II, Adho Mukha Svanasana, and Utthita Trikonasana for strength, balance, and flexibility.");
      }
      else if (age < 18) {
        tips.push("As a young practitioner, practice Vrkshasana, Ananda Balasana, and Balasana to build balance, flexibility, and focus.");
      }
    }

    // --- Gender-based ---
    if (gender === "Female") {
      tips.push("As a female, practice Setu Bandha Sarvangasana, Utkata Konasana, Bhujangasana, Virabhadrasana I & II, Uttanasana, and Tadasana Urdhva Hastasana to improve flexibility, relaxation, posture, and hormonal balance.");
    }
    else if (gender === "Male") {
      tips.push("As a male, practice Virabhadrasana I & II, Phalakasana, Adho Mukha Svanasana, Utthita Trikonasana, Utkatasana, and Setu Bandha Sarvangasana to boost strength, endurance, balance, and overall fitness.");
    }

    // --- Level-based ---
    if (level === "beginner") {
      tips.push("Being a beginner, start with Tadasana, Vrkshasana, Adho Mukha Svanasana, Balasana, and Bitilasana + Marjariasana to build a strong foundation and flexibility.");
    }
    else if (level === "intermediate") {
      tips.push("Being intermediate, practice Virabhadrasana I & II, Utthita Trikonasana, Phalakasana, Setu Bandha Sarvangasana, and Utthita Parsvakonasana to improve stamina, strength, and balance.");
    }
    else if (level === "advanced") {
      tips.push("Being advanced, practice Urdhva Dhanurasana, Natarajasana, Tittibhasana, Utkata Konasana , and Kapotasana  to challenge strength, flexibility, and balance safely.");
    }


    res.json({
      name: user.name,
      wellness: user.wellness,
      tips
    });

  } catch (err) {
    console.error(err);
    res.status(500).json({ message: "Server error" });
  }
});

module.exports = router;