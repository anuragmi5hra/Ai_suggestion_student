const express = require('express');
const router = express.Router();
const OpenAI = require('openai');

// Initialize OpenAI client
const client = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

router.post('/', async (req, res) => {
  try {
    const { title, topic, deadline } = req.body;

    if (!title && !topic) {
      return res.status(400).json({ message: 'Missing required fields' });
    }

    const userPrompt = `
      I have a study task titled "${title}" on topic "${topic}".
      The deadline is ${deadline || "not specified"}.
      Please give me a concise, motivational, and actionable AI suggestion
      to help me complete this task efficiently.
    `;

    // Use GPT model to generate a response
    const completion = await client.chat.completions.create({
      model: "gpt-3.5-turbo",
      messages: [
        { role: "system", content: "You are a helpful AI assistant that gives smart study suggestions." },
        { role: "user", content: userPrompt }
      ],
    });

    const suggestion = completion.choices[0].message.content;

    res.json({ success: true, suggestion });
  } catch (err) {
    console.error("Error generating AI suggestion:", err);
    res.status(500).json({ success: false, message: "Failed to generate suggestion" });
  }
});

module.exports = router;
