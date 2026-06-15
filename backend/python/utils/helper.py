# ============================================================
# utils/helper.py  –  Shared response helpers
# ============================================================
from flask import jsonify

def success(data=None, message="Success", code=200):
    return jsonify({"status": "success", "message": message, "data": data}), code

def error(message="An error occurred", code=400):
    return jsonify({"status": "error", "message": message}), code
