from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import os
from datetime import timedelta
from dotenv import load_dotenv

# Import extensions
from app import db, jwt

# Import models
from app.models.user import User
from app.models.product import Product
from app.models.order import Order

# Import blueprints
from app.routes.auth import auth_bp
from app.routes.products import products_bp
from app.routes.orders import orders_bp
from app.routes.ai_services import ai_services_bp
from app.routes.payments import payments_bp

load_dotenv()

def create_app():
    app = Flask(__name__, static_folder='../frontend/customer')
    
    # Load configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'mysql://username:password@localhost/apex_digital')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-secret-key-change-this')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=30)
    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'your-flask-secret-key')
    
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(products_bp, url_prefix='/api/products')
    app.register_blueprint(orders_bp, url_prefix='/api/orders')
    app.register_blueprint(ai_services_bp, url_prefix='/api/ai')
    app.register_blueprint(payments_bp, url_prefix='/api/payments')
    
    # Serve frontend
    @app.route('/')
    def serve_frontend():
        return send_from_directory(app.static_folder, 'index.html')
    
    @app.route('/<path:path>')
    def serve_static(path):
        return send_from_directory(app.static_folder, path)
    
    # Health check
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({
            "status": "healthy", 
            "service": "Apex Digital",
            "version": "1.0.0"
        })
    
    # Chat endpoint for Robyn AI
    @app.route('/api/ai/chat', methods=['POST'])
    def chat_with_robyn():
        try:
            data = request.get_json()
            message = data.get('message', '')
            
            # Simple AI responses
            responses = {
                'hello': 'Hello! I\'m Robyn, your AI assistant. How can I help you with Apex Digital services today?',
                'hi': 'Hi there! I\'m Robyn. What can I help you with?',
                'price': 'Our prices start from R1299 for content creation up to R12999 for custom AI solutions. All prices are in ZAR.',
                'website': 'We offer Basic Websites from R2499 and E-commerce stores from R5999. Both include AI-powered development.',
                'marketing': 'Our marketing services start from R2999 and include social media management and advertising campaigns.',
                'time': 'Most services are delivered within 3-14 days depending on complexity.',
                'security': 'All our services include military-grade security and compliance with South African regulations.',
                'payment': 'We accept PayFast and other secure payment methods. All transactions are in ZAR.',
                'default': 'I can help you with information about our AI-powered services, pricing, delivery times, and security features. What would you like to know?'
            }
            
            message_lower = message.lower()
            response = responses['default']
            
            for key in responses:
                if key in message_lower and key != 'default':
                    response = responses[key]
                    break
            
            return jsonify({
                'response': response,
                'timestamp': datetime.utcnow().isoformat()
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    # Initialize database
    with app.app_context():
        db.create_all()
        
        # Create default admin user if not exists
        if not User.query.filter_by(email='admin@apexdigital.co.za').first():
            admin = User(
                email='admin@apexdigital.co.za',
                first_name='Admin',
                last_name='User',
                role='admin'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=os.getenv('FLASK_DEBUG', True), host='0.0.0.0', port=5000)
