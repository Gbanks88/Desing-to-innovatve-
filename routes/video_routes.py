from flask import Blueprint, request, jsonify
from services.video_service import VideoService
from utils.decorators import handle_exceptions

video_bp = Blueprint('video', __name__)
video_service = None

def get_service():
    global video_service
    if video_service is None:
        video_service = VideoService()
    return video_service

@video_bp.route('/upload', methods=['POST'])
@handle_exceptions
def upload_video():
    if 'video' not in request.files:
        return jsonify({'error': 'No video file provided'}), 400
        
    file = request.files['video']
    if not file.filename:
        return jsonify({'error': 'No video file selected'}), 400
    
    try:
        video_id = get_service().upload_video(file)
        return jsonify({'id': video_id}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@video_bp.route('/', methods=['GET'])
@handle_exceptions
def get_videos():
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    category = request.args.get('category')
    search_query = request.args.get('q')
    
    videos = get_service().get_videos(page, limit, category, search_query)
    return jsonify(videos)

@video_bp.route('/<video_id>', methods=['GET'])
@handle_exceptions
def get_video(video_id):
    video = get_service().get_video_by_id(video_id)
    if not video:
        return jsonify({"error": "Video not found"}), 404
    return jsonify(video)

@video_bp.route('/<video_id>', methods=['PUT'])
@handle_exceptions
def update_video(video_id):
    data = request.get_json()
    if not validate_video_post(data):
        return jsonify({"error": "Invalid video data"}), 400
    
    result = get_service().update_video(video_id, data)
    if not result:
        return jsonify({"error": "Video not found"}), 404
    return jsonify(result)

@video_bp.route('/<video_id>', methods=['DELETE'])
@handle_exceptions
def delete_video(video_id):
    success = get_service().delete_video(video_id)
    if not success:
        return jsonify({'error': 'Video not found'}), 404
    return jsonify({'message': 'Video deleted successfully'})

@video_bp.route('/search', methods=['GET'])
@handle_exceptions
def search_videos():
    query = request.args.get('q', '')
    videos = get_service().search_videos(query)
    return jsonify({
        'videos': videos,
        'total': len(videos),
        'query': query
    })
