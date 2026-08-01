const express = require('express');
const router = express.Router();
const jwt = require('jsonwebtoken');
const Task = require('../models/Task');

function authMiddleware(req, res, next){
  const auth = req.headers.authorization || '';
  const token = auth.replace('Bearer ', '');
  if(!token) { req.user = null; return next(); }
  try{
    const data = jwt.verify(token, process.env.JWT_SECRET || 'dev');
    req.user = { id: data.id };
  }catch(e){ req.user = null; }
  next();
}

router.use(authMiddleware);

router.get('/', async (req, res)=>{
  try{
    let tasks;
    if(req.user && req.user.id) tasks = await Task.find({ userId: req.user.id }).sort({ createdAt: 1 });
    else tasks = await Task.find({}).sort({ createdAt: 1 });
    res.json({ tasks });
  }catch(e){ console.error(e); res.status(500).json({ message: 'Server error' }); }
});

router.post('/add', async (req, res)=>{
  try{
    const { title, topic, deadline } = req.body;
    const t = new Task({ title, topic, deadline, userId: req.user ? req.user.id : null });
    await t.save();
    res.json({ success: true, task: t });
  }catch(e){ console.error(e); res.status(500).json({ message: 'Server error' }); }
});

module.exports = router;
