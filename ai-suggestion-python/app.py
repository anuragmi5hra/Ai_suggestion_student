from flask import Flask, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import os
import logging

# Import your route blueprints
from auth_routes import auth_bp

# ----------------------------------------
# Flask App Setup
# ----------------------------------------
app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)

# ✅ Load MongoDB URI from environment or fallback
MONGO_URI = os.environ.get(
    "MONGO_URI",
    "mongodb+srv://anuragmishra20006_db_user:anurag9311@anurag.jboglen.mongodb.net/?appName=anurag"
)

# ✅ Connect to MongoDB
try:
    client = MongoClient(MONGO_URI)
    db = client["studyplanner"]
    app.db = db  # Make DB accessible via `current_app.db`
    logging.info("✅ MongoDB connected successfully!")
except Exception as e:
    logging.error(f"❌ MongoDB connection failed: {e}")

# ----------------------------------------
# Register Blueprints
# ----------------------------------------
app.register_blueprint(auth_bp, url_prefix="/api/auth")

# ----------------------------------------
# Default Route
# ----------------------------------------
@app.route("/")
def home():
    return jsonify({"message": "✅ Study Planner Flask API Running with MongoDB!"})

# ----------------------------------------
# Run the App
# ----------------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
