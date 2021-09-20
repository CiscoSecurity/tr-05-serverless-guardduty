from functools import partial
from flask import Blueprint, g
from mappings.mapping import Mapping
from api.observables import Observable
from api.schemas import ObservableSchema
from api.client import GuardDuty
from api.utils import (
    get_json,
    get_jwt,
    jsonify_data,
    remove_duplicates,
    jsonify_result
)

enrich_api = Blueprint('enrich', __name__)

get_observables = partial(get_json, schema=ObservableSchema(many=True))


@enrich_api.route('/observe/observables', methods=['POST'])
def observe_observables():
    _ = get_jwt()
    client = GuardDuty()
    observables = remove_duplicates(get_observables())

    g.sightings = []
    g.indicators = []
    g.relationships = []

    for observable in observables:
        type_, value = observable['type'], observable['value']
        target = Observable.of(type_)
        if target is None:
            continue
        criteria = target.query(value)

        for criterion in criteria:
            client.findings.list_by(criterion)

        findings = client.findings.get()
        for finding in findings:
            mapping = Mapping(finding, **observable)
            with mapping.set_session():
                try:
                    sighting = mapping.extract_sighting()
                    g.sightings.append(sighting.json)

                    indicator = mapping.extract_indicator()
                    g.indicators.append(indicator.json)

                    relationship = mapping.extract_relationship(
                        sighting, indicator, 'sighting-of'
                    )
                    g.relationships.append(relationship.json)
                except KeyError:
                    continue

    return jsonify_result()


@enrich_api.route('/refer/observables', methods=['POST'])
def refer_observables():
    _ = get_jwt()

    observables = get_observables()

    data = []

    for observable in observables:
        type_, value = observable['type'], observable['value']
        observable = Observable.of(type_)
        if observable is None:
            continue

        reference = observable.refer(value, type_)
        data.append(reference)
    return jsonify_data(data)
