from flask import Blueprint

from api.utils import get_jwt, jsonify_data
from api.client import GuardDuty


health_api = Blueprint('health', __name__)


@health_api.route('/health', methods=['POST'])
def health():
    _ = get_jwt()
    client = GuardDuty()
    _ = client.health()
    return jsonify_data({'status': 'ok'})
