// backend/routes/suggest.js
const express = require('express');
const router = express.Router();

router.post('/', async (req, res) => {
  try {
    const { title, topic, deadline } = req.body;

    if (!title && !topic) {
      return res.status(400).json({ message: 'Missing required fields' });
    }

    // Simple example — replace this with your actual AI logic later
    const suggestion = `
      Based on your task "${title || topic}", here’s a helpful suggestion:
      - Break it into smaller sub-tasks.
      - Focus for 25-minute Pomodoro sessions.
      - Try finishing before ${deadline || 'the due date'}.
    `;

    res.json({ success: true, suggestion });
  } catch (err) {
    console.error(err);
    res.status(500).json({ success: false, message: 'Server error' });
  }
});

module.exports = router;
