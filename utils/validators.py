from datetime import datetime
import validators

def validate_fashion_post(data):
    required_fields = ['title', 'description', 'category']
    if not all(field in data for field in required_fields):
        return False
    
    if not isinstance(data.get('tags', []), list):
        return False
    
    return True

def validate_video_post(data):
    required_fields = ['title', 'description', 'category']
    if not all(field in data for field in required_fields):
        return False
    
    if not isinstance(data.get('tags', []), list):
        return False
    
    return True

def validate_scholarship(data):
    required_fields = ['title', 'description', 'amount', 'deadline', 'requirements']
    if not all(field in data for field in required_fields):
        return False
    
    try:
        amount = float(data['amount'])
        if amount <= 0:
            return False
    except (ValueError, TypeError):
        return False
    
    try:
        deadline = datetime.fromisoformat(data['deadline'].replace('Z', '+00:00'))
    except (ValueError, TypeError):
        return False
    
    if not isinstance(data.get('tags', []), list):
        return False
    
    return True
