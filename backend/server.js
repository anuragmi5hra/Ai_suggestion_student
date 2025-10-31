const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const dotenv = require('dotenv');

dotenv.config();
const app = express();

const allowedOrigins = [
  'https://ai-suggestion-student-frontend.onrender.com', // your Render frontend
  'http://localhost:3000', // local dev
  'http://127.0.0.1:3000' // local dev (your case)
];

app.use(cors({
  origin: function (origin, callback) {
    // Allow requests with no origin (like mobile apps or curl)
    if (!origin) return callback(null, true);
    if (allowedOrigins.includes(origin)) {
      return callback(null, true);
    } else {
      return callback(new Error('CORS not allowed for this origin: ' + origin), false);
    }
  },
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'PATCH'],
  credentials: true
}));


app.use(express.json());

const PORT = process.env.PORT || 5000;
const MONGO = process.env.MONGO_URI || 'mongodb://127.0.0.1:27017/studyplanner';

mongoose.connect(MONGO)
  .then(() => console.log('Mongo connected'))
  .catch(e => console.error(e));

app.use('/api/auth', require('./routes/auth'));
app.use('/api/tasks', require('./routes/tasks'));
app.use('/api/suggest', require('./routes/suggest'));

// ✅ Add this route to handle Render root URL
app.get('/', (req, res) => {
  res.send('✅ Backend is running successfully on Render!');
});

app.listen(PORT, () => console.log('Server running on', PORT));
