from flask import Blueprint
from api.utils import get_jwt, jsonify_data
from aws_drivers.aws_guard_duty_driver import GuardDutyDriver


health_api = Blueprint('health', __name__)


@health_api.route('/health', methods=['POST'])
def health():
    _ = get_jwt()
    client = GuardDutyDriver()
    _ = client.health()
    return jsonify_data({'status': 'ok'})
