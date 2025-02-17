from functools import wraps
from flask import request, jsonify, current_app
import jwt
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

def generate_token(user_id: str, expiration_hours: int = 24) -> str:
    """Generate JWT token for user"""
    try:
        payload = {
            'user_id': str(user_id),
            'exp': datetime.utcnow() + timedelta(hours=expiration_hours),
            'iat': datetime.utcnow()
        }
        return jwt.encode(
            payload,
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )
    except Exception as e:
        logger.error(f"Token generation failed: {str(e)}")
        raise

def decode_token(token: str) -> dict:
    """Decode and validate JWT token"""
    try:
        return jwt.decode(
            token,
            current_app.config['SECRET_KEY'],
            algorithms=['HS256']
        )
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")

def require_auth(f):
    """Decorator to require authentication"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Check for token in headers
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({'error': 'Invalid token format'}), 401
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            # Decode and validate token
            payload = decode_token(token)
            request.user_id = payload['user_id']
        except ValueError as e:
            return jsonify({'error': str(e)}), 401
        except Exception as e:
            logger.error(f"Authentication failed: {str(e)}")
            return jsonify({'error': 'Authentication failed'}), 401
        
        return f(*args, **kwargs)
    
    return decorated

def require_role(role):
    """Decorator to require specific role"""
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None
            
            if 'Authorization' in request.headers:
                auth_header = request.headers['Authorization']
                try:
                    token = auth_header.split(" ")[1]
                except IndexError:
                    return jsonify({'error': 'Invalid token format'}), 401
            
            if not token:
                return jsonify({'error': 'Token is missing'}), 401
            
            try:
                # Decode and validate token
                payload = decode_token(token)
                if role not in payload.get('roles', []):
                    return jsonify({'error': 'Insufficient permissions'}), 403
                request.user_id = payload['user_id']
            except ValueError as e:
                return jsonify({'error': str(e)}), 401
            except Exception as e:
                logger.error(f"Role verification failed: {str(e)}")
                return jsonify({'error': 'Authentication failed'}), 401
            
            return f(*args, **kwargs)
        
        return decorated
    return decorator
