from http import HTTPStatus
from unittest.mock import patch
from collections import namedtuple

from pytest import fixture

from tests.unit.api.utils import get_headers
from api.errors import INVALID_ARGUMENT
from tests.unit.conftest import mock_api_response
from tests.unit.payloads_for_tests import (
    EXPECTED_RESPONSE_OF_JWKS_ENDPOINT,
    OBSERVED_TIME,
    DATE_LIST,
    tiles_reponse,
    tile_reponse,
    tile_data_response,
    guard_duty_response
)

WrongCall = \
    namedtuple('WrongCall', ('endpoint', 'payload', 'message'))
SuccessCall = \
    namedtuple('SuccessCall', ('endpoint', 'payload', 'relay_response'))


def wrong_calls():
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
        "last_24_hours, last_7_days, "
        "last_30_days, last_60_days, last_90_days.']}"
    )
    yield WrongCall(
        '/tiles/tile',
        {'tile_id': ''},
        "{'tile_id': ['Field may not be blank.']}"
    )
    yield WrongCall(
        '/tiles/tile',
        {'tile-id': 'some_value'},
        "{'tile_id': ['Missing data for required field.'], "
        "'tile-id': ['Unknown field.']}"
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


def success_calls():
    ids = [
        'affected_instances',
        'events_per_day',
        'top_ten_findings',
        'total_events',
        'port_probe_source_countries'
    ]
    for tile_id in ids:
        yield SuccessCall(
            '/tiles/tile-data',
            {'tile_id': tile_id, 'period': 'last_7_days'},
            tile_data_response(tile_id)
        )
        yield SuccessCall(
            '/tiles/tile',
            {'tile_id': tile_id},
            tile_reponse(tile_id)
        )
    yield SuccessCall(
        '/tiles',
        {},
        tiles_reponse()
    )


@fixture(scope='module', params=success_calls(),
         ids=lambda success_payload: f'{success_payload.endpoint}, '
                                     f'{success_payload.payload}')
def success_call(request):
    return request.param


@patch('requests.get')
@patch('api.client.GuardDuty._look_up_for_data')
@patch('api.tiles.factory.ITile.observed_time')
@patch('api.tiles.events_per_day.EventsPerDayTile._date_list')
def test_dashboard_call_success(mock_dates, mock_time, mock_data, mock_request,
                                success_call, client, valid_jwt):
    mock_request.return_value = \
        mock_api_response(payload=EXPECTED_RESPONSE_OF_JWKS_ENDPOINT)
    mock_data.return_value = \
        guard_duty_response(success_call.payload.get('tile_id'))
    mock_time.return_value = OBSERVED_TIME
    mock_dates.return_value = DATE_LIST
    response = client.post(
        success_call.endpoint, headers=get_headers(valid_jwt()),
        json=success_call.payload
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json == success_call.relay_response
