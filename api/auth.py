"""
API Authentication endpoints with JWT
"""
from flask import jsonify, request
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity, get_jwt
)
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from . import api_bp
from models import db, User


@api_bp.route('/auth/login', methods=['POST'])
def api_login():
    """
    API Login endpoint
    Returns JWT access and refresh tokens
    """
    data = request.get_json()
    
    if not data or not data.get('employee_id') or not data.get('password'):
        return jsonify({'error': 'Missing employee_id or password'}), 400
    
    user = User.query.filter_by(employee_id=data['employee_id']).first()
    
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    if not user.is_active:
        return jsonify({'error': 'Account is disabled'}), 403
    
    # Create tokens with user info
    additional_claims = {
        'employee_id': user.employee_id,
        'name': user.name,
        'role': user.role,
        'department': user.department
    }
    
    access_token = create_access_token(
        identity=user.id,
        additional_claims=additional_claims
    )
    refresh_token = create_refresh_token(identity=user.id)
    
    return jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token,
        'token_type': 'Bearer',
        'user': {
            'id': user.id,
            'employee_id': user.employee_id,
            'name': user.name,
            'email': user.email,
            'department': user.department,
            'role': user.role
        }
    }), 200


@api_bp.route('/auth/refresh', methods=['POST'])
@jwt_required(refresh=True)
def api_refresh():
    """
    Refresh access token using refresh token
    """
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user or not user.is_active:
        return jsonify({'error': 'User not found or inactive'}), 404
    
    additional_claims = {
        'employee_id': user.employee_id,
        'name': user.name,
        'role': user.role,
        'department': user.department
    }
    
    access_token = create_access_token(
        identity=user.id,
        additional_claims=additional_claims
    )
    
    return jsonify({
        'access_token': access_token,
        'token_type': 'Bearer'
    }), 200


@api_bp.route('/auth/logout', methods=['POST'])
@jwt_required()
def api_logout():
    """
    Logout endpoint (client should delete tokens)
    """
    # In a production app, you might want to blacklist the token
    return jsonify({'message': 'Successfully logged out'}), 200


@api_bp.route('/auth/me', methods=['GET'])
@jwt_required()
def api_me():
    """
    Get current user info from JWT token
    """
    current_user_id = get_jwt_identity()
    claims = get_jwt()
    
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({
        'id': user.id,
        'employee_id': user.employee_id,
        'name': user.name,
        'email': user.email,
        'department': user.department,
        'role': user.role,
        'is_active': user.is_active,
        'created_at': user.created_at.isoformat() if user.created_at else None
    }), 200


@api_bp.route('/auth/register', methods=['POST'])
def api_register():
    """
    API Registration endpoint
    """
    data = request.get_json()
    
    required_fields = ['employee_id', 'name', 'email', 'password', 'department']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Check if employee_id already exists
    if User.query.filter_by(employee_id=data['employee_id']).first():
        return jsonify({'error': 'Employee ID already exists'}), 409
    
    # Check if email already exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 409
    
    # Create new user
    user = User(
        employee_id=data['employee_id'],
        name=data['name'],
        email=data['email'],
        password=generate_password_hash(data['password']),
        department=data['department'],
        role=data.get('role', 'user')
    )
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        'message': 'User registered successfully',
        'user': {
            'id': user.id,
            'employee_id': user.employee_id,
            'name': user.name,
            'email': user.email,
            'department': user.department,
            'role': user.role
        }
    }), 201


@api_bp.route('/auth/change-password', methods=['POST'])
@jwt_required()
def api_change_password():
    """
    Change password for authenticated user
    """
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    
    if not data.get('current_password') or not data.get('new_password'):
        return jsonify({'error': 'Missing current_password or new_password'}), 400
    
    # Verify current password
    if not check_password_hash(user.password, data['current_password']):
        return jsonify({'error': 'Current password is incorrect'}), 401
    
    # Update password
    user.password = generate_password_hash(data['new_password'])
    db.session.commit()
    
    return jsonify({'message': 'Password changed successfully'}), 200
