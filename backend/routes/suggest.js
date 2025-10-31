// backend/routes/suggest.js
const express = require("express");
const axios = require("axios");
const router = express.Router();

router.post("/", async (req, res) => {
  try {
    const { title, topic, deadline } = req.body;

    // ✅ Forward the request to the Python backend
    const response = await axios.post(
      "https://your-python-app-url.onrender.com/api/suggest", // 🟢 replace this with your actual deployed Python URL
      { title, topic, deadline }
    );

    // ✅ Send Python response to the frontend
    res.json({ success: true, suggestion: response.data.suggestion });
  } catch (error) {
    console.error("Error communicating with Python API:", error.message);

    // Handle if Python backend returns an error or is unreachable
    res.status(500).json({
      success: false,
      message: "Failed to get suggestion from Python backend",
      details: error.message,
    });
  }
});

module.exports = router;
