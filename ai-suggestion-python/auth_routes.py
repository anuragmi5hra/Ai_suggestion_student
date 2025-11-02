from flask import Blueprint, request, jsonify

auth_bp = Blueprint('auth_bp', __name__)

USERS = {}  # In-memory user store (replace with database later)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'success': False, 'message': 'Email and password required'}), 400

    if email in USERS:
        return jsonify({'success': False, 'message': 'User already exists'}), 400

    USERS[email] = password
    return jsonify({'success': True, 'message': 'Signup successful!'})

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if USERS.get(email) == password:
        return jsonify({'success': True, 'token': 'dummy-token', 'message': 'Login successful'})
    return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
