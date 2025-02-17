from flask import Blueprint, request, jsonify
from services.service_manager import service_manager
from utils.auth import require_auth
from utils.validators import validate_request
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create blueprint
api = Blueprint('api', __name__, url_prefix='/api/john-allens-fashion')

@api.route('/ai/analyze', methods=['POST'])
@require_auth
@validate_request(['image'])
async def analyze_fashion():
    """Analyze fashion image using AI"""
    try:
        result = await service_manager.process_ai_request(
            'fashion_analysis',
            {'image': request.files['image'].read()}
        )
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Fashion analysis failed: {str(e)}")
        return jsonify({'error': str(e)}), 500

@api.route('/ai/recommend', methods=['POST'])
@require_auth
@validate_request(['preferences'])
async def get_recommendations():
    """Get AI-powered fashion recommendations"""
    try:
        result = await service_manager.process_ai_request(
            'outfit_recommendations',
            {'preferences': request.json['preferences']}
        )
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Recommendation generation failed: {str(e)}")
        return jsonify({'error': str(e)}), 500

@api.route('/video/upload', methods=['POST'])
@require_auth
@validate_request(['video', 'metadata'])
async def upload_video():
    """Upload video content"""
    try:
        result = await service_manager.process_video_request(
            'upload',
            {
                'video': request.files['video'].read(),
                'metadata': request.form.get('metadata', {})
            }
        )
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Video upload failed: {str(e)}")
        return jsonify({'error': str(e)}), 500

@api.route('/video/process/<video_id>', methods=['POST'])
@require_auth
@validate_request(['options'])
async def process_video(video_id):
    """Process uploaded video"""
    try:
        result = await service_manager.process_video_request(
            'process',
            {
                'video_id': video_id,
                'options': request.json['options']
            }
        )
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Video processing failed: {str(e)}")
        return jsonify({'error': str(e)}), 500

@api.route('/scholarships/search', methods=['POST'])
@require_auth
@validate_request(['criteria'])
async def search_scholarships():
    """Search for scholarships"""
    try:
        result = await service_manager.process_scholarship_request(
            'search',
            {'criteria': request.json['criteria']}
        )
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Scholarship search failed: {str(e)}")
        return jsonify({'error': str(e)}), 500

@api.route('/scholarships/apply/<scholarship_id>', methods=['POST'])
@require_auth
@validate_request(['application'])
async def apply_scholarship(scholarship_id):
    """Apply for a scholarship"""
    try:
        result = await service_manager.process_scholarship_request(
            'apply',
            {
                'scholarship_id': scholarship_id,
                'application': request.json['application']
            }
        )
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Scholarship application failed: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Error handlers
@api.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad Request', 'message': str(error)}), 400

@api.errorhandler(401)
def unauthorized(error):
    return jsonify({'error': 'Unauthorized', 'message': str(error)}), 401

@api.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not Found', 'message': str(error)}), 404

@api.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Internal Server Error', 'message': str(error)}), 500
