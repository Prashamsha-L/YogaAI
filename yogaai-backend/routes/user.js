const express = require("express");
const router = express.Router();
const User = require("../models/User");
const verifyToken = require("../middleware/auth");

// --- GET user profile ---
router.get("/profile", verifyToken, async (req, res) => {
  try {
    const user = await User.findById(req.user.id);
    if (!user) return res.status(404).json({ message: "User not found" });

    res.json({
      name: user.name,
      email: user.email,
      wellness: user.wellness || {}
    });
  } catch (err) {
    console.error(err);
    res.status(500).json({ message: "Server error" });
  }
});

// --- UPDATE user profile ---
router.put("/profile", verifyToken, async (req, res) => {
  const { name, age, height, weight, gender, level, disease } = req.body;
  try {
    const user = await User.findById(req.user.id);
    if (!user) return res.status(404).json({ message: "User not found" });

    if (name) user.name = name;
    user.wellness = { age, height, weight, gender, level, disease };
    await user.save();

    res.json({ message: "Profile updated successfully", name: user.name, wellness: user.wellness });
  } catch (err) {
    console.error(err);
    res.status(500).json({ message: "Server error" });
  }
});

// --- GET daily calorie/water (today) ---
router.get("/dailyData", verifyToken, async (req, res) => {
  try {
    const user = await User.findById(req.user.id);
    if (!user) return res.status(404).json({ message: "User not found" });

    const today = new Date().toDateString();
    const data = user.dailyData?.get(today) || { calories: { total:0, carbs:0, protein:0, fat:0 }, water:0 };
    res.json(data);
  } catch (err) {
    console.error(err);
    res.status(500).json({ message: "Server error" });
  }
});

router.post("/dailyData", verifyToken, async (req, res) => {
  try {
    const { calories, water } = req.body;
    const user = await User.findById(req.user.id);
    if (!user) return res.status(404).json({ message: "User not found" });

    const today = new Date().toDateString();

    if (!user.dailyData) user.dailyData = new Map();
    user.dailyData.set(today, { calories, water });

    user.markModified('dailyData');  // 🔑 Must mark modified
    await user.save();

    // Convert Map to plain object for response
    const dailyDataObj = Object.fromEntries(user.dailyData);
    res.json({ message: "Daily data saved successfully", dailyData: dailyDataObj });
  } catch (err) {
    console.error(err);
    res.status(500).json({ message: "Server error" });
  }
});

// --- GET last 7 days daily data ---
router.get("/weeklyData", verifyToken, async (req, res) => {
  try {
    const user = await User.findById(req.user.id);
    if (!user) return res.status(404).json({ message: "User not found" });

    const today = new Date();
    const weeklyData = [];

    for (let i = 6; i >= 0; i--) {
      const d = new Date(today);
      d.setDate(today.getDate() - i);
      const dateStr = d.toDateString();
      const dayData = user.dailyData?.get(dateStr) || { calories: { total:0, carbs:0, protein:0, fat:0 }, water:0 };
      weeklyData.push({
        date: dateStr,
        calories: dayData.calories.total,
        water: dayData.water
      });
    }

    res.json(weeklyData);

  } catch (err) {
    console.error(err);
    res.status(500).json({ message: "Server error" });
  }
});

module.exports = router;