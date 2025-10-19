const mongoose = require('mongoose');

const wellnessSchema = new mongoose.Schema({
  age: Number,
  height: Number,
  weight: Number,
  level: String,
  gender: String,
  disease: String
});

const dailyDataSchema = new mongoose.Schema({
  calories: {
    total: { type: Number, default: 0 },
    carbs: { type: Number, default: 0 },
    protein: { type: Number, default: 0 },
    fat: { type: Number, default: 0 }
  },
  water: { type: Number, default: 0 }
});

const userSchema = new mongoose.Schema({
  name: { type: String, required: true },
  email: { type: String, required: true, unique: true },
  password: { type: String, required: true },
  wellness: wellnessSchema,
  dailyData: {
    type: Map,
    of: dailyDataSchema,
    default: () => new Map()
  }
});


module.exports = mongoose.model('User', userSchema);