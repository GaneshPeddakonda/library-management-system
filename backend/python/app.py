# ============================================================
# app.py  –  Main Flask Application Entry Point
# ============================================================
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from flask import Flask, request, jsonify
from flask_cors import CORS

from services.auth_service import AuthService
from controllers.book_controller   import books_bp
from controllers.member_controller import members_bp
from controllers.issue_controller  import issue_bp
from controllers.fine_controller   import fine_bp
from controllers.report_controller import report_bp
from utils.helper import success, error

app = Flask(__name__)
CORS(app)  # Allow frontend requests

# ── Auth routes ────────────────────────────────────────────
@app.route('/api/auth/login', methods=['POST'])
def login():
    d = request.get_json() or {}
    username = d.get('username', '').strip()
    password = d.get('password', '')
    if not username or not password:
        return error("Username and password are required")
    result, err = AuthService.login(username, password)
    if err:
        return error(err, 401)
    return success(result, "Login successful")

@app.route('/api/auth/register', methods=['POST'])
def register():
    d = request.get_json() or {}
    for f in ['username', 'password', 'full_name', 'email']:
        if not d.get(f):
            return error(f"'{f}' is required")
    uid, err = AuthService.register(
        d['username'], d['password'], d['full_name'], d['email'],
        d.get('role', 'member')
    )
    if err:
        return error(f"Registration failed: {err}")
    return success({"id": uid}, "Registered successfully", 201)

# ── Feature blueprints ─────────────────────────────────────
app.register_blueprint(books_bp,   url_prefix='/api/books')
app.register_blueprint(members_bp, url_prefix='/api/members')
app.register_blueprint(issue_bp,   url_prefix='/api/issues')
app.register_blueprint(fine_bp,    url_prefix='/api/fines')
app.register_blueprint(report_bp,  url_prefix='/api/reports')

# ── Health check ───────────────────────────────────────────
@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "message": "Library Management System API"})

# ── Error handlers ─────────────────────────────────────────
@app.errorhandler(404)
def not_found(e):
    return error("Endpoint not found", 404)

@app.errorhandler(500)
def server_error(e):
    return error("Internal server error", 500)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
