from flask import Blueprint, request, jsonify
from services.scholarship_service import ScholarshipService
from utils.decorators import handle_exceptions
from utils.validators import validate_scholarship

scholarship_bp = Blueprint('scholarship', __name__)
scholarship_service = None

def get_service():
    global scholarship_service
    if scholarship_service is None:
        scholarship_service = ScholarshipService()
    return scholarship_service

@scholarship_bp.route('/', methods=['POST'])
@handle_exceptions
def create_scholarship():
    data = request.get_json()
    if not validate_scholarship(data):
        return jsonify({"error": "Invalid scholarship data"}), 400
    
    result = get_service().create_scholarship(data)
    return jsonify(result), 201

@scholarship_bp.route('/search', methods=['GET'])
@handle_exceptions
def search_scholarships():
    query = request.args.get('q', '')
    filters = {
        'min_amount': request.args.get('min_amount', type=float),
        'max_amount': request.args.get('max_amount', type=float),
        'deadline_after': request.args.get('deadline_after'),
        'tags': request.args.getlist('tags')
    }
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    
    scholarships = get_service().search_scholarships(query, filters, page, limit)
    return jsonify(scholarships)

@scholarship_bp.route('/<scholarship_id>', methods=['GET'])
@handle_exceptions
def get_scholarship(scholarship_id):
    scholarship = get_service().get_scholarship_by_id(scholarship_id)
    if not scholarship:
        return jsonify({"error": "Scholarship not found"}), 404
    return jsonify(scholarship)

@scholarship_bp.route('/<scholarship_id>', methods=['PUT'])
@handle_exceptions
def update_scholarship(scholarship_id):
    data = request.get_json()
    if not validate_scholarship(data):
        return jsonify({"error": "Invalid scholarship data"}), 400
    
    result = get_service().update_scholarship(scholarship_id, data)
    if not result:
        return jsonify({"error": "Scholarship not found"}), 404
    return jsonify(result)

@scholarship_bp.route('/<scholarship_id>', methods=['DELETE'])
@handle_exceptions
def delete_scholarship(scholarship_id):
    result = get_service().delete_scholarship(scholarship_id)
    if not result:
        return jsonify({"error": "Scholarship not found"}), 404
    return jsonify({"message": "Scholarship deleted successfully"})

@scholarship_bp.route('/', methods=['GET'])
@handle_exceptions
def list_scholarships():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    filters = {}
    
    # Add filters based on query parameters
    if request.args.get('amount_min'):
        filters['amount'] = {'$gte': float(request.args.get('amount_min'))}
    if request.args.get('amount_max'):
        if 'amount' in filters:
            filters['amount']['$lte'] = float(request.args.get('amount_max'))
        else:
            filters['amount'] = {'$lte': float(request.args.get('amount_max'))}
    if request.args.get('deadline'):
        filters['deadline'] = {'$gte': request.args.get('deadline')}
    if request.args.get('category'):
        filters['category'] = request.args.get('category')
    
    scholarships, total = get_service().list_scholarships(page, per_page, filters)
    return jsonify({
        'scholarships': scholarships,
        'total': total,
        'page': page,
        'per_page': per_page,
        'filters': filters
    })

@scholarship_bp.route('/search', methods=['GET'])
@handle_exceptions
def search_scholarships():
    query = request.args.get('q', '')
    scholarships = get_service().search_scholarships(query)
    return jsonify({
        'scholarships': scholarships,
        'total': len(scholarships),
        'query': query
    })
