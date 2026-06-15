# services/auth_service.py
import jwt, bcrypt
from datetime import datetime, timedelta
from utils.db_connection import execute_query
from config import SECRET_KEY, JWT_EXPIRY_HOURS

class AuthService:
    @staticmethod
    def login(username, password):
        rows = execute_query(
            "SELECT * FROM users WHERE username=%s", (username,)
        )
        if not rows:
            return None, "Invalid username or password"
        user = rows[0]
        if not bcrypt.checkpw(password.encode(), user['password'].encode()):
            return None, "Invalid username or password"
        token = jwt.encode({
            "user_id": user['id'],
            "username": user['username'],
            "role": user['role'],
            "exp": datetime.utcnow() + timedelta(hours=JWT_EXPIRY_HOURS)
        }, SECRET_KEY, algorithm="HS256")
        return {"token": token, "user": {
            "id": user['id'], "username": user['username'],
            "full_name": user['full_name'], "role": user['role']
        }}, None

    @staticmethod
    def register(username, password, full_name, email, role="member"):
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        try:
            uid = execute_query(
                "INSERT INTO users (username,password,full_name,email,role) VALUES (%s,%s,%s,%s,%s)",
                (username, hashed, full_name, email, role),
                fetch=False
            )
            return uid, None
        except Exception as e:
            return None, str(e)

    @staticmethod
    def verify_token(token):
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=["HS256"]), None
        except jwt.ExpiredSignatureError:
            return None, "Token expired"
        except jwt.InvalidTokenError:
            return None, "Invalid token"
