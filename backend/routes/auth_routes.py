from flask import Blueprint, request, jsonify
from models.user_model import User
from utils.db import get_db
from flask_jwt_extended import create_access_token

# Blueprint for authentication routes
auth_blueprint = Blueprint('auth', __name__)

# Route for user registration
@auth_blueprint.route('/register', methods=['POST'])
def register():
    db = get_db()
    data = request.get_json()

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # Validate email format
    if not User.validate_email(email):
        return jsonify({'message': 'Invalid email format'}), 400
    
    # Check if username or email already exists
    if db.users.find_one({'username': username}):
        return jsonify({'message': 'Username already exists'}), 400
    if db.users.find_one({'email': email}):
        return jsonify({'message': 'Email already exists'}), 400
    
    # Create new user and save to database
    new_user = User(username=username, email=email, password=password)
    db.users.insert_one(new_user.to_dict())

    return jsonify({'message': 'User registered successfully!'}), 201

# Route for user login
@auth_blueprint.route('/login', methods=['POST'])
def login():
    db = get_db()
    data = request.get_json()
    identifier = data.get('email')
    password = data.get('password')

    # Find user by email
    user_data = db.users.find_one({'email': identifier})

    if not user_data:
        return jsonify({'message': 'Invalid credentials'}), 401
    
    # Create User object from DB data
    user = User.from_dict(user_data)

    # Check password validity
    if not user.check_password(password):
        return jsonify({'message': 'Invalid password'}), 401
    
    # Generate JWT token for valid user
    access_token = create_access_token(identity=user.username)
    return jsonify({'access_token': access_token}), 200
