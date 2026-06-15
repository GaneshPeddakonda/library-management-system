# controllers/report_controller.py
from flask import Blueprint
from services.report_service import ReportService
from utils.helper import success
from controllers.auth_middleware import token_required

report_bp = Blueprint('report', __name__)

@report_bp.route('/stats', methods=['GET'])
@token_required
def dashboard_stats(current_user):
    return success(ReportService.dashboard_stats())

@report_bp.route('/popular-books', methods=['GET'])
@token_required
def popular_books(current_user):
    return success(ReportService.popular_books())

@report_bp.route('/active-members', methods=['GET'])
@token_required
def active_members(current_user):
    return success(ReportService.active_members())
