const express = require('express');
const router = express.Router();
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const User = require('../models/User');

router.post('/signup', async (req, res)=>{
  const { name, email, password } = req.body;
  if(!email || !password) return res.json({ message: 'Missing fields' });
  try{
    let user = await User.findOne({ email });
    if(user) return res.json({ message: 'User exists' });
    const hash = await bcrypt.hash(password, 10);
    user = new User({ name, email, passwordHash: hash });
    await user.save();
    const token = jwt.sign({ id: user._id }, process.env.JWT_SECRET || 'dev', { expiresIn: '7d' });
    res.json({ token });
  }catch(e){ console.error(e); res.status(500).json({ message: 'Server error' }); }
});

router.post('/login', async (req, res)=>{
  const { email, password } = req.body;
  if(!email || !password) return res.json({ message: 'Missing fields' });
  try{
    const user = await User.findOne({ email });
    if(!user) return res.json({ message: 'Invalid credentials' });
    const ok = await bcrypt.compare(password, user.passwordHash);
    if(!ok) return res.json({ message: 'Invalid credentials' });
    const token = jwt.sign({ id: user._id }, process.env.JWT_SECRET || 'dev', { expiresIn: '7d' });
    res.json({ token });
  }catch(e){ console.error(e); res.status(500).json({ message: 'Server error' }); }
});

module.exports = router;
