"""
API endpoints for overtime management
"""
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from datetime import datetime, date

from . import api_bp
from models import db, OvertimeRequest, User


@api_bp.route('/overtime', methods=['GET'])
@jwt_required()
def get_overtime_requests():
    """
    Get overtime requests for current user
    Query params: status, date_from, date_to
    """
    current_user_id = get_jwt_identity()
    claims = get_jwt()
    
    query = OvertimeRequest.query.filter_by(user_id=current_user_id)
    
    # Filter by status
    status = request.args.get('status')
    if status:
        query = query.filter_by(status=status)
    
    # Filter by date range
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    if date_from:
        query = query.filter(OvertimeRequest.date >= date_from)
    if date_to:
        query = query.filter(OvertimeRequest.date <= date_to)
    
    requests = query.order_by(OvertimeRequest.created_at.desc()).all()
    
    return jsonify({
        'requests': [{
            'id': req.id,
            'date': req.date.isoformat(),
            'start_time': req.start_time.strftime('%H:%M'),
            'end_time': req.end_time.strftime('%H:%M'),
            'reason': req.reason,
            'status': req.status,
            'created_at': req.created_at.isoformat() if req.created_at else None,
            'approved_at': req.approved_at.isoformat() if req.approved_at else None
        } for req in requests]
    }), 200


@api_bp.route('/overtime', methods=['POST'])
@jwt_required()
def create_overtime_request():
    """
    Create new overtime request
    """
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    required_fields = ['date', 'start_time', 'end_time', 'reason']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        overtime = OvertimeRequest(
            user_id=current_user_id,
            date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
            start_time=datetime.strptime(data['start_time'], '%H:%M').time(),
            end_time=datetime.strptime(data['end_time'], '%H:%M').time(),
            reason=data['reason'],
            status='pending'
        )
        
        db.session.add(overtime)
        db.session.commit()
        
        return jsonify({
            'message': 'Overtime request created successfully',
            'request': {
                'id': overtime.id,
                'date': overtime.date.isoformat(),
                'start_time': overtime.start_time.strftime('%H:%M'),
                'end_time': overtime.end_time.strftime('%H:%M'),
                'reason': overtime.reason,
                'status': overtime.status
            }
        }), 201
        
    except ValueError as e:
        return jsonify({'error': f'Invalid date/time format: {str(e)}'}), 400


@api_bp.route('/overtime/<int:request_id>', methods=['PUT'])
@jwt_required()
def update_overtime_request(request_id):
    """
    Update overtime request (only if pending)
    """
    current_user_id = get_jwt_identity()
    overtime = OvertimeRequest.query.filter_by(
        id=request_id,
        user_id=current_user_id
    ).first()
    
    if not overtime:
        return jsonify({'error': 'Request not found'}), 404
    
    if overtime.status != 'pending':
        return jsonify({'error': 'Can only update pending requests'}), 400
    
    data = request.get_json()
    
    try:
        if 'date' in data:
            overtime.date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        if 'start_time' in data:
            overtime.start_time = datetime.strptime(data['start_time'], '%H:%M').time()
        if 'end_time' in data:
            overtime.end_time = datetime.strptime(data['end_time'], '%H:%M').time()
        if 'reason' in data:
            overtime.reason = data['reason']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Overtime request updated successfully',
            'request': {
                'id': overtime.id,
                'date': overtime.date.isoformat(),
                'start_time': overtime.start_time.strftime('%H:%M'),
                'end_time': overtime.end_time.strftime('%H:%M'),
                'reason': overtime.reason,
                'status': overtime.status
            }
        }), 200
        
    except ValueError as e:
        return jsonify({'error': f'Invalid date/time format: {str(e)}'}), 400


@api_bp.route('/overtime/<int:request_id>', methods=['DELETE'])
@jwt_required()
def delete_overtime_request(request_id):
    """
    Delete overtime request (only if pending)
    """
    current_user_id = get_jwt_identity()
    overtime = OvertimeRequest.query.filter_by(
        id=request_id,
        user_id=current_user_id
    ).first()
    
    if not overtime:
        return jsonify({'error': 'Request not found'}), 404
    
    if overtime.status != 'pending':
        return jsonify({'error': 'Can only delete pending requests'}), 400
    
    db.session.delete(overtime)
    db.session.commit()
    
    return jsonify({'message': 'Overtime request deleted successfully'}), 200


@api_bp.route('/overtime/<int:request_id>/approve', methods=['POST'])
@jwt_required()
def approve_overtime_request(request_id):
    """
    Approve overtime request (admin only)
    """
    current_user_id = get_jwt_identity()
    claims = get_jwt()
    
    if claims.get('role') != 'admin':
        return jsonify({'error': 'Admin access required'}), 403
    
    overtime = OvertimeRequest.query.get(request_id)
    
    if not overtime:
        return jsonify({'error': 'Request not found'}), 404
    
    if overtime.status != 'pending':
        return jsonify({'error': 'Request is not pending'}), 400
    
    overtime.status = 'approved'
    overtime.approved_by = current_user_id
    overtime.approved_at = datetime.utcnow()
    
    db.session.commit()
    
    return jsonify({
        'message': 'Overtime request approved',
        'request': {
            'id': overtime.id,
            'status': overtime.status,
            'approved_at': overtime.approved_at.isoformat()
        }
    }), 200


@api_bp.route('/overtime/<int:request_id>/reject', methods=['POST'])
@jwt_required()
def reject_overtime_request(request_id):
    """
    Reject overtime request (admin only)
    """
    current_user_id = get_jwt_identity()
    claims = get_jwt()
    
    if claims.get('role') != 'admin':
        return jsonify({'error': 'Admin access required'}), 403
    
    overtime = OvertimeRequest.query.get(request_id)
    
    if not overtime:
        return jsonify({'error': 'Request not found'}), 404
    
    if overtime.status != 'pending':
        return jsonify({'error': 'Request is not pending'}), 400
    
    overtime.status = 'rejected'
    overtime.approved_by = current_user_id
    overtime.approved_at = datetime.utcnow()
    
    db.session.commit()
    
    return jsonify({
        'message': 'Overtime request rejected',
        'request': {
            'id': overtime.id,
            'status': overtime.status,
            'approved_at': overtime.approved_at.isoformat()
        }
    }), 200
