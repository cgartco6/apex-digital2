from app import db
from datetime import datetime
import json

class AIService(db.Model):
    __tablename__ = 'ai_services'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    agent_type = db.Column(db.String(50), nullable=False)  # content, marketing, security, etc.
    capabilities = db.Column(db.JSON)  # List of capabilities
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'agent_type': self.agent_type,
            'capabilities': self.capabilities or [],
            'is_active': self.is_active
        }

class AITask(db.Model):
    __tablename__ = 'ai_tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    service_type = db.Column(db.String(50), nullable=False)
    task_data = db.Column(db.JSON, nullable=False)  # Input data for the task
    status = db.Column(db.String(50), default='pending')  # pending, processing, completed, failed
    result_data = db.Column(db.JSON)  # Output data from AI
    progress = db.Column(db.Integer, default=0)  # 0-100%
    assigned_agents = db.Column(db.JSON)  # List of agent IDs working on this
    error_message = db.Column(db.Text)
    started_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'service_type': self.service_type,
            'task_data': self.task_data or {},
            'status': self.status,
            'result_data': self.result_data or {},
            'progress': self.progress,
            'assigned_agents': self.assigned_agents or [],
            'error_message': self.error_message,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'created_at': self.created_at.isoformat()
        }
