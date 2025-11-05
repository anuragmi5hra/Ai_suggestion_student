from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import os
from bson import ObjectId

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)

# -------------------- DATABASE SETUP --------------------
MONGO_URI = os.environ.get("MONGO_URI", "mongodb+srv://anuragmishra20006_db_user:anurag9311@anurag.jboglen.mongodb.net/?appName=anurag")

try:
    client = MongoClient(MONGO_URI)
    db = client["studyplanner"]
    users = db["users"]
    tasks = db["tasks"]
    print("✅ MongoDB connected successfully!")
except Exception as e:
    print("❌ MongoDB connection failed:", e)


# -------------------- FRONTEND ROUTES --------------------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/suggestions")
def suggestions():
    return render_template("suggestions.html")

@app.route("/progress")
def progress():
    return render_template("progress.html")


# -------------------- TASK ROUTES --------------------
@app.route("/tasks", methods=["GET"])
def get_tasks():
    task_list = []
    for t in db.tasks.find():
        t["_id"] = str(t["_id"])  # Convert ObjectId to string
        task_list.append(t)
    return jsonify({"tasks": task_list}), 200


@app.route("/tasks/add", methods=["POST"])
def add_task():
    data = request.get_json()
    title = data.get("title")
    topic = data.get("topic")
    deadline = data.get("deadline")

    if not all([title, topic, deadline]):
        return jsonify({"success": False, "message": "All fields required"}), 400

    db.tasks.insert_one({
        "title": title,
        "topic": topic,
        "deadline": deadline,
        "progress": 0,
        "done": False
    })
    return jsonify({"success": True, "message": "Task added successfully"}), 201


@app.route("/tasks/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    result = db.tasks.delete_one({"_id": ObjectId(task_id)})
    if result.deleted_count == 0:
        return jsonify({"success": False, "message": "Task not found"}), 404
    return jsonify({"success": True, "message": "Task deleted"}), 200


@app.route("/tasks/<task_id>/progress", methods=["PATCH"])
def update_progress(task_id):
    task = db.tasks.find_one({"_id": ObjectId(task_id)})
    if not task:
        return jsonify({"success": False, "message": "Task not found"}), 404

    new_progress = min(task.get("progress", 0) + 10, 100)
    db.tasks.update_one({"_id": ObjectId(task_id)}, {"$set": {"progress": new_progress}})
    return jsonify({"success": True, "message": "Progress updated"}), 200


@app.route("/tasks/<task_id>/done", methods=["PATCH"])
def mark_done(task_id):
    result = db.tasks.update_one({"_id": ObjectId(task_id)}, {"$set": {"done": True, "progress": 100}})
    if result.matched_count == 0:
        return jsonify({"success": False, "message": "Task not found"}), 404
    return jsonify({"success": True, "message": "Task marked as done"}), 200


# -------------------- AI SUGGESTION ROUTE --------------------
@app.route("/suggest", methods=["POST"])
def suggest():
    data = request.get_json()
    title = data.get("title")
    topic = data.get("topic")
    deadline = data.get("deadline")

    # Simple logic for suggestion (you can expand this later)
    suggestion = f"For your topic '{topic}', try revising key notes for 30 minutes daily before {deadline}."

    return jsonify({"suggestion": suggestion}), 200


# -------------------- AUTH ROUTES --------------------
@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    name, email, password = data.get("name"), data.get("email"), data.get("password")

    if not all([name, email, password]):
        return jsonify({"message": "All fields required"}), 400

    if db.users.find_one({"email": email}):
        return jsonify({"message": "User already exists"}), 400

    db.users.insert_one({"name": name, "email": email, "password": password})
    return jsonify({"message": "Signup successful"}), 201


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email, password = data.get("email"), data.get("password")

    user = db.users.find_one({"email": email, "password": password})
    if not user:
        return jsonify({"message": "Invalid email or password"}), 401

    return jsonify({"message": "Login successful", "name": user["name"]}), 200


# -------------------- MAIN --------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
