# controllers/fine_controller.py
from flask import Blueprint
from models.fine import Fine
from utils.helper import success, error
from controllers.auth_middleware import token_required

fine_bp = Blueprint('fine', __name__)

@fine_bp.route('/', methods=['GET'])
@token_required
def get_fines(current_user):
    return success(Fine.get_all())

@fine_bp.route('/pay/<int:fine_id>', methods=['POST'])
@token_required
def pay_fine(current_user, fine_id):
    Fine.pay(fine_id)
    return success(None, "Fine marked as paid")
