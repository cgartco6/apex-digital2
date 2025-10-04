from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.utils.generators import generate_order_number
import datetime

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('/', methods=['POST'])
@jwt_required()
def create_order():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data or 'items' not in data or not data['items']:
            return jsonify({'error': 'No items in order'}), 400
        
        # Calculate total and validate products
        total_amount = 0
        order_items = []
        
        for item in data['items']:
            product = Product.query.get(item['product_id'])
            if not product or not product.is_active:
                return jsonify({'error': f'Product {item["product_id"]} not found'}), 404
            
            quantity = item.get('quantity', 1)
            total_amount += product.price * quantity
            
            order_items.append(OrderItem(
                product_id=product.id,
                quantity=quantity,
                price=product.price,
                configuration=item.get('configuration', {})
            ))
        
        # Create order
        order = Order(
            user_id=user_id,
            order_number=generate_order_number(),
            total_amount=total_amount,
            client_requirements=data.get('requirements', {}),
            status='pending',
            payment_status='pending'
        )
        
        order.items = order_items
        db.session.add(order)
        db.session.commit()
        
        return jsonify({
            'message': 'Order created successfully',
            'order': order.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@orders_bp.route('/', methods=['GET'])
@jwt_required()
def get_user_orders():
    try:
        user_id = get_jwt_identity()
        orders = Order.query.filter_by(user_id=user_id).order_by(Order.created_at.desc()).all()
        
        return jsonify({
            'orders': [order.to_dict() for order in orders]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@orders_bp.route('/<int:order_id>', methods=['GET'])
@jwt_required()
def get_order(order_id):
    try:
        user_id = get_jwt_identity()
        order = Order.query.filter_by(id=order_id, user_id=user_id).first()
        
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        
        return jsonify({'order': order.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
