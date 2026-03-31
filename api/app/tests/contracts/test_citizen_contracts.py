import pytest
from app.tests.api_test_support import assert_json_response, json_of
from app.tests.contracts.conftest import validate_schema
from app.tests.contracts.schemas import (
    CITIZEN_RESPONSE_SCHEMA,
    SERVICE_REQUEST_LIST_RESPONSE_SCHEMA,
)

pytestmark = [pytest.mark.contracts, pytest.mark.usefixtures("seeded_database")]


def _create_citizen(api_client, position, *, name):
    response = api_client.post(
        f"/citizens/{position}/add_citizen/",
        json={"citizen_name": name},
    )
    assert_json_response(response, 201)
    return json_of(response)["citizen"]


def _create_service_request(api_client, citizen_id, seeded_data):
    response = api_client.post(
        "/service_requests/",
        json={
            "service_request": {
                "citizen_id": citizen_id,
                "service_id": seeded_data["service_ids"]["ptax"],
                "channel_id": seeded_data["channel_ids"]["phone"],
                "quantity": 2,
            }
        },
    )
    assert_json_response(response, 201)
    return json_of(response)["service_request"]


def test_citizen_detail_matches_the_nested_contract(internal_ga_client, seeded_data):
    """Assert that citizen detail preserves the nested queue-state contract used by the frontend."""
    citizen = _create_citizen(internal_ga_client, 0, name="Contract Citizen")
    _create_service_request(internal_ga_client, citizen["citizen_id"], seeded_data)

    response = internal_ga_client.get(f"/citizens/{citizen['citizen_id']}/")
    body = json_of(response)

    assert_json_response(response, 200)
    validate_schema(body, CITIZEN_RESPONSE_SCHEMA)

    citizen_detail = body["citizen"]
    service_request = citizen_detail["service_reqs"][0]
    period = service_request["periods"][0]

    assert citizen_detail["start_time"].endswith("Z")
    assert citizen_detail["cs"]["cs_state_name"] == "Active"
    assert service_request["sr_state"]["sr_code"] == "Active"
    assert period["ps"]["ps_name"] == "Ticket Creation"
    assert isinstance(period["csr"]["counter_id"], int)


def test_citizen_service_requests_endpoint_matches_the_nested_contract(
    internal_ga_client, seeded_data
):
    """Assert that the citizen service-request list returns the expected nested contract."""
    citizen = _create_citizen(internal_ga_client, 0, name="Contract Requests Citizen")
    service_request = _create_service_request(
        internal_ga_client, citizen["citizen_id"], seeded_data
    )

    response = internal_ga_client.get(
        f"/citizens/{citizen['citizen_id']}/service_requests/"
    )
    body = json_of(response)

    assert_json_response(response, 200)
    validate_schema(body, SERVICE_REQUEST_LIST_RESPONSE_SCHEMA)

    request_body = body["service_requests"][0]
    assert request_body["sr_id"] == service_request["sr_id"]
    assert request_body["sr_state"]["sr_code"] == "Active"
    assert request_body["periods"][0]["ps"]["ps_name"] == "Ticket Creation"
