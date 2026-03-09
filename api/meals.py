"""
API endpoints for meal registration
"""
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

from . import api_bp
from models import db, MealRegistration


@api_bp.route('/meals', methods=['GET'])
@jwt_required()
def get_meal_registrations():
    """
    Get meal registrations for current user
    Query params: date_from, date_to
    """
    current_user_id = get_jwt_identity()
    
    query = MealRegistration.query.filter_by(user_id=current_user_id)
    
    # Filter by date range
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    if date_from:
        query = query.filter(MealRegistration.date >= date_from)
    if date_to:
        query = query.filter(MealRegistration.date <= date_to)
    
    registrations = query.order_by(MealRegistration.date.desc()).all()
    
    return jsonify({
        'registrations': [{
            'id': reg.id,
            'date': reg.date.isoformat(),
            'meal_type': reg.meal_type,
            'has_meal': reg.has_meal,
            'notes': reg.notes,
            'created_at': reg.created_at.isoformat() if reg.created_at else None
        } for reg in registrations]
    }), 200


@api_bp.route('/meals', methods=['POST'])
@jwt_required()
def create_meal_registration():
    """
    Create or update meal registration
    """
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data.get('date'):
        return jsonify({'error': 'Missing date field'}), 400
    
    try:
        meal_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        
        # Check if registration already exists
        existing = MealRegistration.query.filter_by(
            user_id=current_user_id,
            date=meal_date
        ).first()
        
        if existing:
            # Update existing
            existing.has_meal = data.get('has_meal', True)
            existing.meal_type = data.get('meal_type')
            existing.notes = data.get('notes', '')
            db.session.commit()
            
            return jsonify({
                'message': 'Meal registration updated',
                'registration': {
                    'id': existing.id,
                    'date': existing.date.isoformat(),
                    'has_meal': existing.has_meal,
                    'meal_type': existing.meal_type,
                    'notes': existing.notes
                }
            }), 200
        else:
            # Create new
            registration = MealRegistration(
                user_id=current_user_id,
                date=meal_date,
                has_meal=data.get('has_meal', True),
                meal_type=data.get('meal_type'),
                notes=data.get('notes', '')
            )
            
            db.session.add(registration)
            db.session.commit()
            
            return jsonify({
                'message': 'Meal registration created',
                'registration': {
                    'id': registration.id,
                    'date': registration.date.isoformat(),
                    'has_meal': registration.has_meal,
                    'meal_type': registration.meal_type,
                    'notes': registration.notes
                }
            }), 201
            
    except ValueError as e:
        return jsonify({'error': f'Invalid date format: {str(e)}'}), 400


@api_bp.route('/meals/<int:registration_id>', methods=['DELETE'])
@jwt_required()
def delete_meal_registration(registration_id):
    """
    Delete meal registration
    """
    current_user_id = get_jwt_identity()
    registration = MealRegistration.query.filter_by(
        id=registration_id,
        user_id=current_user_id
    ).first()
    
    if not registration:
        return jsonify({'error': 'Registration not found'}), 404
    
    db.session.delete(registration)
    db.session.commit()
    
    return jsonify({'message': 'Meal registration deleted successfully'}), 200
