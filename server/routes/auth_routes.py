from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from ..models.models import User, db
from werkzeug.security import check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}

    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    phone = data.get('phone')
    address = data.get('address')

    # Validate input
    if not name or not email or not password:
        return jsonify({'error': 'Name, email, and password are required.'}), 400

    # Check if user already exists
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered.'}), 400

    try:
        user = User(
            name=name,
            email=email,
            password=password,
            phone=phone,
            address=address
        )
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Registration failed.', 'details': str(e)}), 500

    access_token = create_access_token(identity=user.id)
    return jsonify({
        'message': 'User registered successfully.',
        'user': user.to_dict(),
        'access_token': access_token
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required.'}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({'error': 'Invalid credentials.'}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify({
        'message': 'Logged in successfully.',
        'user': user.to_dict(),
        'access_token': access_token
    }), 200

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found.'}), 404
    return jsonify(user.to_dict()), 200

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    # JWT is stateless; logout is handled client-side by removing the token
    return jsonify({'message': 'Logged out successfully.'}), 200