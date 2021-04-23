from functools import partial
from api.mapping import Mapping
from api.observables import Observable
from api.schemas import ObservableSchema
from flask import Blueprint, g, current_app
from aws_drivers.aws_guard_duty_driver import GuardDutyDriver
from api.utils import (
    get_json,
    get_jwt,
    jsonify_data,
    remove_duplicates,
    jsonify_result
)


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
    observables = remove_duplicates(get_observables())

    g.verdicts = []
    g.judgements = []
    g.sightings = []

    for observable in observables:
        type_, value = observable.values()
        observable = Observable.of(type_)
        if observable is None:
            continue
        criterion = observable.query(value)

        mapping = Mapping(type_, value)
        findings = guard_duty.findings.get(criterion)

        for finding in findings:
            g.sightings.append(mapping.sighting.extract(finding))

    return jsonify_result()


@enrich_api.route('/refer/observables', methods=['POST'])
def refer_observables():
    _ = get_jwt()

    observables = get_observables()

    data = []

    url = current_app.config['GUARD_DUTY_REFER_URL']

    for observable in observables:
        type_, value = observable.values()
        observable = Observable.of(type_)
        if observable is None:
            continue

        reference = observable.refer(url, value)
        data.append(reference)
    return jsonify_data(data)
