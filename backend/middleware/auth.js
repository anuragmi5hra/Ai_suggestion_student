const express = require("express");
const router = express.Router();
const bcrypt = require("bcryptjs");
const jwt = require("jsonwebtoken");
const User = require("../models/User");

// SIGNUP
router.post("/signup", async (req, res) => {
  const { name, email, password } = req.body;
  if (!email || !password) return res.status(400).json({ message: "Missing fields" });

  try {
    let user = await User.findOne({ email });
    if (user) return res.status(400).json({ message: "User already exists" });

    const hash = await bcrypt.hash(password, 10);
    user = new User({ name, email, password: hash }); // ✅ match schema
    await user.save();

    const token = jwt.sign({ id: user._id }, process.env.JWT_SECRET || "dev", { expiresIn: "7d" });
    res.status(201).json({ token, user: { id: user._id, name: user.name, email: user.email } });
  } catch (e) {
    console.error("Signup error:", e);
    res.status(500).json({ message: "Server error" });
  }
});

// LOGIN
router.post("/login", async (req, res) => {
  const { email, password } = req.body;
  if (!email || !password) return res.status(400).json({ message: "Missing fields" });

  try {
    const user = await User.findOne({ email });
    if (!user) return res.status(401).json({ message: "Invalid credentials" });

    const ok = await bcrypt.compare(password, user.password); // ✅ match schema
    if (!ok) return res.status(401).json({ message: "Invalid credentials" });

    const token = jwt.sign({ id: user._id }, process.env.JWT_SECRET || "dev", { expiresIn: "7d" });
    res.json({ token, user: { id: user._id, name: user.name, email: user.email } });
  } catch (e) {
    console.error("Login error:", e);
    res.status(500).json({ message: "Server error" });
  }
});

module.exports = router;
