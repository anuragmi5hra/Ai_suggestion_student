from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'success': False, 'message': 'Email and password required'}), 400

    db = current_app.config["db"]
    users = db.users

    if users.find_one({'email': email}):
        return jsonify({'success': False, 'message': 'User already exists'}), 400

    hashed_pw = generate_password_hash(password)
    users.insert_one({'email': email, 'password': hashed_pw})
    return jsonify({'success': True, 'message': 'Signup successful!'})

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    db = current_app.config["db"]
    users = db.users

    user = users.find_one({'email': email})
    if user and check_password_hash(user['password'], password):
        return jsonify({'success': True, 'token': 'dummy-token', 'message': 'Login successful'})
    
    return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
