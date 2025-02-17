from flask import Blueprint, request, jsonify
from services.fashion_service import FashionService
from utils.validators import validate_fashion_post

fashion_bp = Blueprint('fashion', __name__)
fashion_service = None

def get_service():
    global fashion_service
    if fashion_service is None:
        fashion_service = FashionService()
    return fashion_service

@fashion_bp.route('/', methods=['POST'])
def create_fashion_post():
    data = request.get_json()
    if not validate_fashion_post(data):
        return jsonify({"error": "Invalid fashion post data"}), 400
    
    result = get_service().create_post(data)
    return jsonify(result), 201

@fashion_bp.route('/', methods=['GET'])
def get_fashion_posts():
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    category = request.args.get('category')
    search_query = request.args.get('q')
    
    posts = get_service().get_posts(page, limit, category, search_query)
    return jsonify(posts)

@fashion_bp.route('/<post_id>', methods=['GET'])
def get_fashion_post(post_id):
    post = get_service().get_post_by_id(post_id)
    if not post:
        return jsonify({"error": "Post not found"}), 404
    return jsonify(post)

@fashion_bp.route('/<post_id>', methods=['PUT'])
def update_fashion_post(post_id):
    data = request.get_json()
    if not validate_fashion_post(data):
        return jsonify({"error": "Invalid fashion post data"}), 400
    
    result = get_service().update_post(post_id, data)
    if not result:
        return jsonify({"error": "Post not found"}), 404
    return jsonify(result)

@fashion_bp.route('/<post_id>', methods=['DELETE'])
def delete_fashion_post(post_id):
    result = get_service().delete_post(post_id)
    if not result:
        return jsonify({"error": "Post not found"}), 404
    return jsonify({"message": "Post deleted successfully"})
