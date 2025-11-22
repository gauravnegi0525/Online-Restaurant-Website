from flask import Blueprint, request, jsonify
from server.models.models import MenuItem, User, db
from flask_jwt_extended import jwt_required, get_jwt_identity

menu_bp = Blueprint('menu', __name__)

@menu_bp.route('/', methods=['GET'])
def get_menu_items():
    category = request.args.get('category')
    query = MenuItem.query

    if category:
        query = query.filter_by(category=category)

    menu_items = query.all()
    return jsonify([item.to_dict() for item in menu_items]), 200

@menu_bp.route('/<int:item_id>', methods=['GET'])
def get_menu_item(item_id):
    item = MenuItem.query.get(item_id)
    if not item:
        return jsonify({'error': 'Menu item not found'}), 404
    return jsonify(item.to_dict()), 200

@menu_bp.route('/', methods=['POST'])
@jwt_required()
def create_menu_item():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if not user or not user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.get_json() or {}

    required_fields = ['name', 'description', 'price', 'category', 'image']
    if not all(field in data and data[field] for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        item = MenuItem(
            name=data['name'],
            description=data['description'],
            price=float(data['price']),
            category=data['category'],
            image=data['image'],
            is_featured=bool(data.get('is_featured', False))
        )
        db.session.add(item)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create menu item.', 'details': str(e)}), 500

    return jsonify(item.to_dict()), 201

@menu_bp.route('/<int:item_id>', methods=['PUT'])
@jwt_required()
def update_menu_item(item_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if not user or not user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403

    item = MenuItem.query.get(item_id)
    if not item:
        return jsonify({'error': 'Menu item not found'}), 404

    data = request.get_json() or {}

    if 'name' in data and data['name']:
        item.name = data['name']
    if 'description' in data and data['description']:
        item.description = data['description']
    if 'price' in data and data['price']:
        try:
            item.price = float(data['price'])
        except ValueError:
            return jsonify({'error': 'Invalid price value.'}), 400
    if 'category' in data and data['category']:
        item.category = data['category']
    if 'image' in data and data['image']:
        item.image = data['image']
    if 'is_featured' in data:
        item.is_featured = bool(data['is_featured'])

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update menu item.', 'details': str(e)}), 500

    return jsonify(item.to_dict()), 200

@menu_bp.route('/<int:item_id>', methods=['DELETE'])
@jwt_required()
def delete_menu_item(item_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if not user or not user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403

    item = MenuItem.query.get(item_id)
    if not item:
        return jsonify({'error': 'Menu item not found'}), 404

    try:
        db.session.delete(item)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete menu item.', 'details': str(e)}), 500

    return jsonify({'message': 'Menu item deleted successfully'}), 200