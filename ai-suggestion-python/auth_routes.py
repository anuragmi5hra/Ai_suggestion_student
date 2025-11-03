from flask import Blueprint, request, jsonify, current_app

auth_bp = Blueprint('auth_bp', __name__)

# ----------------------------------------
# Signup Route
# ----------------------------------------
@auth_bp.route("/signup", methods=["POST"])
def signup():
    db = current_app.db
    data = request.get_json()
    name, email, password = data.get("name"), data.get("email"), data.get("password")

    if not all([name, email, password]):
        return jsonify({"message": "All fields are required"}), 400

    if db.users.find_one({"email": email}):
        return jsonify({"message": "User already exists"}), 400

    db.users.insert_one({"name": name, "email": email, "password": password})
    return jsonify({"message": "Signup successful"}), 201

# ----------------------------------------
# Login Route
# ----------------------------------------
@auth_bp.route("/login", methods=["POST"])
def login():
    db = current_app.db
    data = request.get_json()
    email, password = data.get("email"), data.get("password")

    user = db.users.find_one({"email": email, "password": password})
    if not user:
        return jsonify({"message": "Invalid email or password"}), 401

    return jsonify({
        "message": "Login successful",
        "user": user["name"]
    }), 200
