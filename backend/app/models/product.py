from app import db
from datetime import datetime

class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    short_description = db.Column(db.String(500))
    price = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default='ZAR')
    category = db.Column(db.String(100), nullable=False)
    service_type = db.Column(db.String(50))  # website, marketing, content, etc.
    delivery_days = db.Column(db.Integer, default=7)
    image_url = db.Column(db.String(500))
    features = db.Column(db.JSON)  # List of features
    requirements = db.Column(db.JSON)  # Client requirements needed
    is_active = db.Column(db.Boolean, default=True)
    ai_generated = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    order_items = db.relationship('OrderItem', backref='product', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'short_description': self.short_description,
            'price': self.price,
            'currency': self.currency,
            'category': self.category,
            'service_type': self.service_type,
            'delivery_days': self.delivery_days,
            'image_url': self.image_url,
            'features': self.features or [],
            'requirements': self.requirements or [],
            'is_active': self.is_active
        }
