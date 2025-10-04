from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token
import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')

CORS(app)
jwt = JWTManager(app)

# Import routes
from routes.auth import auth_bp
from routes.products import products_bp
from routes.orders import orders_bp
from routes.ai_agents import ai_agents_bp

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(products_bp, url_prefix='/api/products')
app.register_blueprint(orders_bp, url_prefix='/api/orders')
app.register_blueprint(ai_agents_bp, url_prefix='/api/ai')

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "service": "Apex Digital"})

if __name__ == '__main__':
    app.run(debug=os.getenv('FLASK_DEBUG', False))
