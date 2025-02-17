from functools import wraps

def handle_exceptions(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            return {"error": str(e)}, 500
    return wrapper
