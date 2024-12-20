from flask import Blueprint, request, jsonify
from models.user_model import User
from utils.db import get_db
from flask_jwt_extended import create_access_token

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/register', methods = ['POST'])
def register():
    db = get_db()
    data = request.get_json()

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not User.validate_email(email):
        return jsonify({'message': 'Invalid email format'}), 400
    
    if db.users.find_one({'username': username}):
        return jsonify({'message': 'Username already exists'}), 400
    if db.users.find_one({'email': email}):
        return jsonify({'message': 'Email already exists'}), 400
    
    new_user = User(username=username, email=email, password=password)
    db.users.insert_one(new_user.to_dict())

    return jsonify({'message': 'User registered successfully!'}), 201

@auth_blueprint.route('/login', methods = ['POST'])
def login():
    db = get_db()
    data = request.get_json()
    identifier = data.get('email')
    password = data.get('password')

    user_data = db.users.find_one(
        {'email': identifier}
        )

    if not user_data:
        return jsonify({'message': 'Invalid credentials'}), 401
    
    user = User.from_dict(user_data)

    if not user.check_password(password):
        return jsonify({'message': 'Invalid password'}), 401
    
    access_token = create_access_token(identity = user.username)
    return jsonify({'access_token' : access_token}), 200
