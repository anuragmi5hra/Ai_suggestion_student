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

// +10% Progress
router.patch('/:id/progress', async (req, res) => {
  try {
    const { id } = req.params;
    const task = await Task.findById(id);
    if (!task) return res.status(404).json({ message: 'Task not found' });

    task.progress = Math.min(100, (task.progress || 0) + 10);
    await task.save();

    res.json({ success: true, task });
  } catch (e) {
    console.error('🔥 Error in /:id/progress:', e);
    res.status(500).json({ message: 'Server error' });
  }
});

// Mark as done (100%)
router.patch('/:id/done', async (req, res) => {
  try {
    const { id } = req.params;
    const task = await Task.findById(id);
    if (!task) return res.status(404).json({ message: 'Task not found' });

    task.progress = 100;
    await task.save();

    res.json({ success: true, task });
  } catch (e) {
    console.error('🔥 Error in /:id/done:', e);
    res.status(500).json({ message: 'Server error' });
  }
});

router.delete('/:id', authMiddleware, async (req, res) => {
  try {
    const task = await Task.findByIdAndDelete(req.params.id);
    if (!task) return res.status(404).json({ success: false, message: 'Task not found' });
    res.json({ success: true, message: 'Task deleted' });
  } catch (err) {
    res.status(500).json({ success: false, message: 'Server error' });
  }
});

module.exports = router;
