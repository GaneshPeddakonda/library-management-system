# controllers/member_controller.py
from flask import Blueprint, request
from models.member import Member
from utils.helper import success, error
from controllers.auth_middleware import token_required

members_bp = Blueprint('members', __name__)

@members_bp.route('/', methods=['GET'])
@token_required
def get_members(current_user):
    return success(Member.get_all())

@members_bp.route('/<int:member_id>', methods=['GET'])
@token_required
def get_member(current_user, member_id):
    m = Member.get_by_id(member_id)
    return success(m) if m else error("Member not found", 404)

@members_bp.route('/', methods=['POST'])
@token_required
def add_member(current_user):
    d = request.get_json() or {}
    for f in ['full_name', 'email']:
        if not d.get(f):
            return error(f"'{f}' is required")
    mid = Member.create(d['full_name'], d['email'], d.get('phone',''), d.get('address',''))
    return success({"id": mid}, "Member added", 201)

@members_bp.route('/<int:member_id>', methods=['PUT'])
@token_required
def update_member(current_user, member_id):
    d = request.get_json() or {}
    allowed = ['full_name','email','phone','address','status']
    fields = {k: v for k, v in d.items() if k in allowed}
    if not fields:
        return error("No valid fields")
    Member.update(member_id, **fields)
    return success(None, "Member updated")

@members_bp.route('/<int:member_id>', methods=['DELETE'])
@token_required
def delete_member(current_user, member_id):
    Member.delete(member_id)
    return success(None, "Member deleted")
