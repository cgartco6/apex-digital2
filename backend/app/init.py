from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    # Load configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600  # 1 hour
    
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    CORS(app)
    
    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.products import products_bp
    from app.routes.orders import orders_bp
    from app.routes.ai_services import ai_services_bp
    from app.routes.payments import payments_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(products_bp, url_prefix='/api/products')
    app.register_blueprint(orders_bp, url_prefix='/api/orders')
    app.register_blueprint(ai_services_bp, url_prefix='/api/ai')
    app.register_blueprint(payments_bp, url_prefix='/api/payments')
    
    return app
