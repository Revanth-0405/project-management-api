from functools import wraps
from flask import request,jsonify

def require_fields(*fields):
    def decorator(f):
        @wraps(f)
        def wrapper(*args,**kwargs):
            data=request.get_json()
            if not data:
                return jsonify({"error":"JSON body required"}),400
            for field in fields:
                if field not in data:
                    return jsonify({"error":f"{field} required"}),400
            return f(*args,**kwargs)
        return wrapper
    return decorator
