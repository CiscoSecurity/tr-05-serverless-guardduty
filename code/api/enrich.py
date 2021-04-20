from functools import partial
from api.observables import Observable
from api.schemas import ObservableSchema
from flask import Blueprint,  current_app, g
from aws_drivers.aws_guard_duty_driver import GuardDutyDriver
from api.utils import get_json, get_jwt, jsonify_data, filter_observables


enrich_api = Blueprint('enrich', __name__)

get_observables = partial(get_json, schema=ObservableSchema(many=True))


@enrich_api.route('/deliberate/observables', methods=['POST'])
def deliberate_observables():
    _ = get_jwt()
    _ = get_observables()
    return jsonify_data({})


@enrich_api.route('/observe/observables', methods=['POST'])
def observe_observables():
    _ = get_jwt()
    guard_duty = GuardDutyDriver()
    observables = filter_observables(get_observables())

    g.verdicts = []
    g.judgements = []
    g.sightings = []

    for observable in observables:
        type_ = observable['type']
        value = observable['value']
        observable = Observable.of(type_=type_)
        criterion = observable.query(observable=value)
        findings = guard_duty.findings.get(criterion)

        for finding in findings:
            g.sightings.append()

    return jsonify_data({})


@enrich_api.route('/refer/observables', methods=['POST'])
def refer_observables():
    _ = get_jwt()
    _ = get_observables()
    return jsonify_data([])
