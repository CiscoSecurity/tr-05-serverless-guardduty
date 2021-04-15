from api.observables import Observable
from flask import Blueprint, current_app
from api.utils import get_jwt, jsonify_data
from aws_drivers.aws_guard_duty_driver import GuardDutyDriver


health_api = Blueprint('health', __name__)


@health_api.route('/health', methods=['POST'])
def health():
    _ = get_jwt()
    GDD = GuardDutyDriver()
    type_, value = current_app.config['HEALTH_CHECK_OBSERVABLE'].values()

    observable = Observable.of(type_)
    condition = observable.query(value)

    GDD.findings.list(current_app.config['AWS_GUARD_DUTY_DETECTOR_ID'], condition)

    return jsonify_data({'status': 'ok'})
