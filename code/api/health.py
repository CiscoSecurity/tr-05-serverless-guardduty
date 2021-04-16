from flask import Blueprint
from api.observables import Observable
from api.utils import get_jwt, jsonify_data
from aws_drivers.aws_guard_duty_driver import GuardDutyDriver


health_api = Blueprint('health', __name__)


@health_api.route('/health', methods=['POST'])
def health():
    _ = get_jwt()
    guard_duty = GuardDutyDriver()
    observable = Observable.of(type_='ip')
    criterion = observable.query(observable='1.1.1.1')
    _ = guard_duty.findings.list(criterion)

    return jsonify_data({'status': 'ok'})
