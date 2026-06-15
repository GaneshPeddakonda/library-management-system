# controllers/issue_controller.py
from flask import Blueprint, request
from services.issue_service import IssueService
from utils.helper import success, error
from controllers.auth_middleware import token_required

issue_bp = Blueprint('issue', __name__)

@issue_bp.route('/', methods=['GET'])
@token_required
def get_issues(current_user):
    return success(IssueService.get_active_issues())

@issue_bp.route('/overdue', methods=['GET'])
@token_required
def get_overdue(current_user):
    return success(IssueService.get_overdue())

@issue_bp.route('/', methods=['POST'])
@token_required
def issue_book(current_user):
    d = request.get_json() or {}
    book_id   = d.get('book_id')
    member_id = d.get('member_id')
    if not book_id or not member_id:
        return error("book_id and member_id are required")
    result, err = IssueService.issue_book(book_id, member_id, current_user['user_id'])
    if err:
        return error(err)
    return success(result, "Book issued successfully", 201)

@issue_bp.route('/return/<int:issue_id>', methods=['POST'])
@token_required
def return_book(current_user, issue_id):
    result, err = IssueService.return_book(issue_id)
    if err:
        return error(err)
    msg = f"Book returned. Fine: ₹{result['fine']}" if result['fine'] else "Book returned successfully"
    return success(result, msg)
