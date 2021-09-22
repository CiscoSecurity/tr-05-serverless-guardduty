from pytest import fixture
from http import HTTPStatus
from .utils import get_headers
from unittest.mock import patch
from collections import namedtuple
from api.errors import INVALID_ARGUMENT
from tests.unit.conftest import mock_api_response
from tests.unit.payloads_for_tests import (
    EXPECTED_RESPONSE_OF_JWKS_ENDPOINT,
    TILES_RESPONSE,
    AFFECTED_INSTANCES_CRITERIA,
    tile_data_response,
    guard_duty_response
)


WrongCall = namedtuple('WrongCall', ('endpoint', 'payload', 'message'))


def wrong_calls():
    yield WrongCall(
        '/tiles/tile',
        {'tile-id': 'some_value'},
        "{'tile_id': ['Missing data for required field.'], "
        "'tile-id': ['Unknown field.']}"
    )
    yield WrongCall(
        '/tiles/tile',
        {'tile_id': ''},
        "{'tile_id': ['Field may not be blank.']}"
    )
    yield WrongCall(
        '/tiles/tile-data',
        {'tile-id': 'some_value', 'period': 'last_7_days'},
        "{'tile_id': ['Missing data for required field.'], "
        "'tile-id': ['Unknown field.']}"
    )
    yield WrongCall(
        '/tiles/tile-data',
        {'tile_id': '', 'period': 'last_7_days'},
        "{'tile_id': ['Field may not be blank.']}"
    )
    yield WrongCall(
        '/tiles/tile-data',
        {'tile_id': 'some_value', 'not_period': 'last_7_days'},
        "{'period': ['Missing data for required field.'], "
        "'not_period': ['Unknown field.']}"
    )
    yield WrongCall(
        '/tiles/tile-data',
        {'tile_id': 'some_value', 'period': ''},
        "{'period': ['Must be one of: "
        "last_24_hours, last_7_days, last_30_days.']}"
    )


@fixture(
    scope='module',
    params=wrong_calls(),
    ids=lambda wrong_payload: f'{wrong_payload.endpoint}, '
                              f'{wrong_payload.payload}'
)
def wrong_call(request):
    return request.param


@fixture(scope='module')
def invalid_argument_expected_payload():
    def _make_message(message):
        return {
            'errors': [{
                'code': INVALID_ARGUMENT,
                'message': message,
                'type': 'fatal'
            }]
        }

    return _make_message


@patch('requests.get')
def test_dashboard_call_with_wrong_payload(mock_request,
                                           wrong_call, client, valid_jwt,
                                           invalid_argument_expected_payload):
    mock_request.return_value = \
        mock_api_response(payload=EXPECTED_RESPONSE_OF_JWKS_ENDPOINT)

    response = client.post(
        path=wrong_call.endpoint,
        headers=get_headers(valid_jwt()),
        json=wrong_call.payload
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json == invalid_argument_expected_payload(
        wrong_call.message
    )


def routes():
    yield '/tiles'
    yield '/tiles/tile'
    yield '/tiles/tile-data'


@fixture(scope='module', params=routes(), ids=lambda route: f'POST {route}')
def route(request):
    return request.param


@fixture(scope='module')
def valid_json():
    return {"period": "last_7_days", "tile_id": "affected_instances"}


@patch('requests.get')
@patch('api.client.GuardDuty._look_up_for_data')
@patch('api.charts.AffectedInstances.criterion')
def test_dashboard_call_success(mock_criteria, mock_data, mock_request,
                                route, client, valid_jwt,
                                valid_json):
    mock_request.return_value = \
        mock_api_response(payload=EXPECTED_RESPONSE_OF_JWKS_ENDPOINT)
    if route == '/tiles':
        response = client.post(route, headers=get_headers(valid_jwt()))
        assert response.status_code == HTTPStatus.OK
        assert response.json == TILES_RESPONSE
    if route == '/tiles/tile-data':
        mock_data.return_value = guard_duty_response()
        mock_criteria.return_value = AFFECTED_INSTANCES_CRITERIA
        response = client.post(
            route, headers=get_headers(valid_jwt()), json=valid_json
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json == tile_data_response()
