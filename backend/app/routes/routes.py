from flask import Blueprint, request, jsonify
from app import db
from app.models.product import Product

products_bp = Blueprint('products', __name__)

@products_bp.route('/', methods=['GET'])
def get_products():
    try:
        category = request.args.get('category')
        service_type = request.args.get('service_type')
        
        query = Product.query.filter_by(is_active=True)
        
        if category:
            query = query.filter_by(category=category)
        if service_type:
            query = query.filter_by(service_type=service_type)
        
        products = query.all()
        
        return jsonify({
            'products': [product.to_dict() for product in products]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@products_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    try:
        product = Product.query.get(product_id)
        
        if not product or not product.is_active:
            return jsonify({'error': 'Product not found'}), 404
        
        return jsonify({'product': product.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@products_bp.route('/categories', methods=['GET'])
def get_categories():
    try:
        categories = db.session.query(Product.category).distinct().filter_by(is_active=True).all()
        categories = [cat[0] for cat in categories if cat[0]]
        
        return jsonify({'categories': categories}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
