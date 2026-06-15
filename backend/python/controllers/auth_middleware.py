# controllers/auth_middleware.py
from functools import wraps
from flask import request
from services.auth_service import AuthService
from utils.helper import error

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization', '')
        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
        if not token:
            return error("Token is missing", 401)
        payload, err = AuthService.verify_token(token)
        if err:
            return error(err, 401)
        return f(payload, *args, **kwargs)
    return decorated
