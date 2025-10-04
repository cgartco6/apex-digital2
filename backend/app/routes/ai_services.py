from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.ai_service import AIService, AITask
from app.agents.content_creator import ContentCreationAgent
from app.agents.marketing_pro import MarketingAgent
from app.agents.website_builder import WebsiteBuilderAgent
import asyncio

ai_services_bp = Blueprint('ai_services', __name__)

@ai_services_bp.route('/services', methods=['GET'])
def get_ai_services():
    try:
        services = AIService.query.filter_by(is_active=True).all()
        
        return jsonify({
            'services': [service.to_dict() for service in services]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ai_services_bp.route('/process-task', methods=['POST'])
@jwt_required()
def process_ai_task():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data or 'service_type' not in data or 'task_data' not in data:
            return jsonify({'error': 'Missing service_type or task_data'}), 400
        
        # Create AI task record
        ai_task = AITask(
            user_id=user_id,
            order_id=data.get('order_id'),
            service_type=data['service_type'],
            task_data=data['task_data'],
            status='pending'
        )
        
        db.session.add(ai_task)
        db.session.commit()
        
        # Process task based on service type
        if data['service_type'] == 'content_creation':
            agent = ContentCreationAgent()
        elif data['service_type'] == 'marketing':
            agent = MarketingAgent()
        elif data['service_type'] == 'website_builder':
            agent = WebsiteBuilderAgent()
        else:
            return jsonify({'error': 'Unsupported service type'}), 400
        
        # Process task asynchronously
        asyncio.create_task(process_task_async(ai_task.id, agent, data['task_data']))
        
        return jsonify({
            'message': 'AI task started',
            'task_id': ai_task.id
        }), 202
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

async def process_task_async(task_id, agent, task_data):
    from app import db
    from app.models.ai_service import AITask
    
    try:
        # Update task status
        task = AITask.query.get(task_id)
        task.status = 'processing'
        task.started_at = datetime.utcnow()
        db.session.commit()
        
        # Process task
        result = await agent.process_task(task_data)
        
        # Update task with result
        task.status = 'completed'
        task.result_data = result
        task.progress = 100
        task.completed_at = datetime.utcnow()
        db.session.commit()
        
    except Exception as e:
        task = AITask.query.get(task_id)
        task.status = 'failed'
        task.error_message = str(e)
        db.session.commit()
