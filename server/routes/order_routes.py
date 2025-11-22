from flask import Blueprint, request, jsonify
from ..models.models import Order, OrderItem, MenuItem, User, db
from flask_jwt_extended import jwt_required, get_jwt_identity

order_bp = Blueprint('orders', __name__)

@order_bp.route('/', methods=['GET'])
@jwt_required()
def get_orders():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    if user.is_admin:
        orders = Order.query.all()
    else:
        orders = Order.query.filter_by(user_id=current_user_id).all()

    return jsonify([order.to_dict() for order in orders]), 200

@order_bp.route('/', methods=['POST'])
@jwt_required()
def create_order():
    current_user_id = get_jwt_identity()
    data = request.get_json() or {}

    required_fields = ['items', 'delivery_address', 'phone', 'payment_method']
    if not all(field in data and data[field] for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    items = data['items']
    if not isinstance(items, list) or len(items) == 0:
        return jsonify({'error': 'Invalid items'}), 400

    total_amount = 0
    order_items = []

    for item_data in items:
        menu_item_id = item_data.get('menu_item_id')
        quantity = item_data.get('quantity')
        if not menu_item_id or not quantity:
            return jsonify({'error': 'Invalid item format'}), 400

        menu_item = MenuItem.query.get(menu_item_id)
        if not menu_item:
            return jsonify({'error': f'Menu item {menu_item_id} not found'}), 404

        try:
            quantity = int(quantity)
        except ValueError:
            return jsonify({'error': 'Quantity must be an integer'}), 400

        if quantity <= 0:
            return jsonify({'error': 'Quantity must be positive'}), 400

        total_amount += menu_item.price * quantity
        order_items.append({
            'menu_item': menu_item,
            'quantity': quantity,
            'price': menu_item.price
        })

    try:
        order = Order(
            user_id=current_user_id,
            total_amount=total_amount,
            delivery_address=data['delivery_address'],
            phone=data['phone'],
            payment_method=data['payment_method'],
            payment_status='pending'
        )
        db.session.add(order)
        db.session.commit()

        for item in order_items:
            order_item = OrderItem(
                order_id=order.id,
                menu_item_id=item['menu_item'].id,
                quantity=item['quantity'],
                price=item['price']
            )
            db.session.add(order_item)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create order.', 'details': str(e)}), 500

    return jsonify(order.to_dict()), 201

@order_bp.route('/<int:order_id>', methods=['GET'])
@jwt_required()
def get_order(order_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    order = Order.query.get(order_id)

    if not order:
        return jsonify({'error': 'Order not found'}), 404

    # Admins can view all orders, users only their own
    if not user or (not user.is_admin and order.user_id != current_user_id):
        return jsonify({'error': 'Unauthorized'}), 403

    return jsonify(order.to_dict()), 200

@order_bp.route('/<int:order_id>/status', methods=['PUT'])
@jwt_required()
def update_order_status(order_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    order = Order.query.get(order_id)

    if not order:
        return jsonify({'error': 'Order not found'}), 404

    if not user or not user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.get_json() or {}

    if not data.get('status'):
        return jsonify({'error': 'Missing status'}), 400

    order.status = data['status']

    if 'payment_status' in data:
        order.payment_status = data['payment_status']

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update order status.', 'details': str(e)}), 500

    return jsonify(order.to_dict()), 200