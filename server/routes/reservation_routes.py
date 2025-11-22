from flask import Blueprint, request, jsonify
from ..models.models import Reservation, User, db
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

reservation_bp = Blueprint('reservations', __name__)

@reservation_bp.route('/', methods=['GET'])
@jwt_required()
def get_reservations():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    if user.is_admin:
        reservations = Reservation.query.all()
    else:
        reservations = Reservation.query.filter_by(user_id=current_user_id).all()

    return jsonify([res.to_dict() for res in reservations]), 200

@reservation_bp.route('/', methods=['POST'])
@jwt_required()
def create_reservation():
    current_user_id = get_jwt_identity()
    data = request.get_json() or {}

    required_fields = ['name', 'email', 'phone', 'date', 'time', 'guests']
    if not all(field in data and data[field] for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        date = datetime.strptime(data['date'], '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400

    try:
        reservation = Reservation(
            user_id=current_user_id,
            name=data['name'],
            email=data['email'],
            phone=data['phone'],
            date=date,
            time=data['time'],
            guests=data['guests'],
            special_requests=data.get('special_requests'),
            status='pending'
        )
        db.session.add(reservation)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create reservation.', 'details': str(e)}), 500

    return jsonify(reservation.to_dict()), 201

@reservation_bp.route('/<int:reservation_id>', methods=['PUT'])
@jwt_required()
def update_reservation(reservation_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    reservation = Reservation.query.get(reservation_id)

    if not reservation:
        return jsonify({'error': 'Reservation not found'}), 404

    if reservation.user_id != current_user_id and not (user and user.is_admin):
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.get_json() or {}

    if 'date' in data and data['date']:
        try:
            reservation.date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400

    if 'time' in data and data['time']:
        reservation.time = data['time']
    if 'guests' in data and data['guests']:
        reservation.guests = data['guests']
    if 'special_requests' in data:
        reservation.special_requests = data['special_requests']
    if 'status' in data and user and user.is_admin:
        reservation.status = data['status']

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update reservation.', 'details': str(e)}), 500

    return jsonify(reservation.to_dict()), 200

@reservation_bp.route('/<int:reservation_id>', methods=['DELETE'])
@jwt_required()
def cancel_reservation(reservation_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    reservation = Reservation.query.get(reservation_id)

    if not reservation:
        return jsonify({'error': 'Reservation not found'}), 404

    # Admins can cancel any reservation, users only their own
    if reservation.user_id != current_user_id and not (user and user.is_admin):
        return jsonify({'error': 'Unauthorized'}), 403

    reservation.status = 'cancelled'
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to cancel reservation.', 'details': str(e)}), 500

    return jsonify({'message': 'Reservation cancelled successfully'}), 200