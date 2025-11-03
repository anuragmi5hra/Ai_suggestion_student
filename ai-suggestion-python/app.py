from flask import Flask, jsonify
from flask_cors import CORS
import logging, os
from pymongo import MongoClient

# Import route blueprints
from auth_routes import auth_bp
from task_routes import task_bp
from suggestion_routes import suggest_bp

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)

# ✅ MongoDB Connection
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://127.0.0.1:27017/studyplanner")
client = MongoClient(MONGO_URI)
db = client["studyplanner"]

# ✅ Share DB with routes
app.config["db"] = db

# ✅ CORS setup
CORS(app, resources={r"/*": {
    "origins": [
        "http://127.0.0.1:3000",
        "http://localhost:3000",
        "https://ai-suggestion-student-frontend.onrender.com"
    ]
}}, supports_credentials=True)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(task_bp, url_prefix="/api/tasks")
app.register_blueprint(suggest_bp, url_prefix="/api")

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS')
    return response

@app.route('/')
def home():
    return jsonify({"message": "✅ Study Planner + AI Suggestion API is running successfully!"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
