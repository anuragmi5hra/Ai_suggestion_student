from flask import Blueprint, request, jsonify
from pymongo import MongoClient
import os

auth_bp = Blueprint('auth_bp', __name__)

# ✅ Connect MongoDB
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["studyplanner"]
users_collection = db["users"]

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'success': False, 'message': 'Email and password required'}), 400

    if users_collection.find_one({'email': email}):
        return jsonify({'success': False, 'message': 'User already exists'}), 400

    users_collection.insert_one({'name': name, 'email': email, 'password': password})
    return jsonify({'success': True, 'message': 'Signup successful!'})

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    user = users_collection.find_one({'email': email, 'password': password})
    if not user:
        return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

    return jsonify({'success': True, 'token': 'dummy-token', 'message': 'Login successful'})
