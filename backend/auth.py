from flask import Blueprint
from flask_jwt_extended  import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask import Flask, request, jsonify
from backend.models import db, User, Course, Enrollment
from werkzeug.security import generate_password_hash, check_password_hash
from textwrap import fill


auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['POST'])
def register():
    data = request.json
    # using .get instead of [] whcih throws an error if the key is not found
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    # list of complusory field that users must fill in and check if those field are filled in.
    required = ['username', 'password', 'email']
    for field in required:
        if field not in data:
            return jsonify({"msg": f"Missing {field}"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"msg": "User already exists"}), 400
    
    if User.query.filter_by(email=email).first():
            return jsonify({"msg": "Email already exists"}), 400
    
    hashed_password = generate_password_hash(password)
    user = User(username=username, password=hashed_password, email=email)
    db.session.add(user)
    db.session.commit()

    return jsonify({"msg": "User registered successfully"}), 201


@auth.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()

    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({"msg": "Invalid credentials"}), 401

    token = create_access_token(identity=user.id)
    return jsonify({"token": token})
