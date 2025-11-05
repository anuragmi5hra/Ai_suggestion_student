from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import os

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)

# MongoDB connection
MONGO_URI = os.environ.get("MONGO_URI", "mongodb+srv://anuragmishra20006_db_user:anurag9311@anurag.jboglen.mongodb.net/?appName=anurag")

try:
    client = MongoClient(MONGO_URI)
    db = client["studyplanner"]
    users = db["users"]
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
    tasks = list(db.tasks.find({}, {"_id": 0}))
    return jsonify(tasks)

@app.route("/tasks/add", methods=["POST"])
def add_task():
    data = request.get_json()
    title = data.get("title")
    subject = data.get("subject")
    deadline = data.get("deadline")

    if not all([title, subject, deadline]):
        return jsonify({"error": "All fields required"}), 400

    db.tasks.insert_one({"title": title, "subject": subject, "deadline": deadline})
    return jsonify({"message": "Task added successfully"}), 201



# -------------------- BACKEND ROUTES --------------------
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
