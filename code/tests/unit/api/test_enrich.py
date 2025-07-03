from http import HTTPStatus
from unittest.mock import patch

from pytest import fixture

from tests.unit.api.utils import get_headers
from tests.unit.conftest import mock_api_response
from tests.unit.payloads_for_tests import (
    OBSERVE_RESPONSE,
    REFER_RESPONSE,
    guard_duty_response
)


def routes():
    yield '/observe/observables'
    yield '/refer/observables'


def ids():
    yield 'transient:aws-guard-duty' \
          '-sighting-099065c8932f41e29083ed7a742cb644'
    yield 'transient:aws-guard-duty' \
          '-indicator-f001da94620f4d2e8f0fe6d29629e618'
    yield 'transient:aws-guard-duty' \
          '-relationship-08c0d67d19e5483998953246c094fe0d'
    yield 'transient:aws-guard-duty' \
          '-sighting-bc0af638cea2466cb74e34d4dcd3fc4b'
    yield 'transient:aws-guard-duty' \
          '-indicator-88c24095ae564d5795cc3f08992e5898'
    yield 'transient:aws-guard-duty' \
          '-relationship-10774be950d74376bc1bd90a98e89d21'


@fixture(scope='module', params=routes(), ids=lambda route: f'POST {route}')
def route(request):
    return request.param


@fixture(scope='module')
def invalid_json_value():
    return [{'type': 'ip', 'value': ''}]


@patch('requests.get')
def test_enrich_call_with_valid_jwt_but_invalid_json_value(
        mock_request,
        route, client, valid_jwt, invalid_json_value,
        invalid_json_expected_payload, test_keys_and_token
):
    mock_request.return_value = \
        mock_api_response(payload=test_keys_and_token["jwks"])
    response = client.post(route,
                           headers=get_headers(valid_jwt()),
                           json=invalid_json_value)
    assert response.status_code == HTTPStatus.OK
    assert response.json == invalid_json_expected_payload(
        "{0: {'value': ['Field may not be blank.']}}"
    )


@fixture(scope='module')
def valid_json():
    return [{'type': 'ip', 'value': '10.0.0.1'}]


@patch('requests.get')
@patch('api.client.GuardDuty._look_up_for_data')
@patch('bundlebuilder.models.entity.PrimaryEntity._generate_transient_id')
def test_enrich_call_success(mock_id, mock_data, mock_request,
                             route, client, valid_jwt, valid_json, test_keys_and_token):
    mock_request.return_value = \
        mock_api_response(payload=test_keys_and_token["jwks"])
    mock_data.return_value = guard_duty_response()
    mock_id.side_effect = ids()
    response = client.post(route, headers=get_headers(valid_jwt()),
                           json=valid_json)
    assert response.status_code == HTTPStatus.OK
    if route == "/refer/observables":
        assert response.json == REFER_RESPONSE
    if route == "/observe/observables":
        assert response.json == OBSERVE_RESPONSE
