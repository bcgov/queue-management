import pytest
from app.utilities.timezone_utils import local_datetime_to_utc
from app.tests.api_test_support import (
    assert_json_response,
    future_utc_window,
    json_of,
    unique_name,
)
from app.tests.contracts.conftest import validate_schema
from app.tests.contracts.schemas import BOOKING_LIST_RESPONSE_SCHEMA, BOOKING_RESPONSE_SCHEMA

pytestmark = [pytest.mark.contracts, pytest.mark.usefixtures("seeded_database")]


def _create_booking(api_client, seeded_data, *, days_from_now):
    start_time, end_time = future_utc_window(days_from_now, duration_minutes=120)
    response = api_client.post(
        "/bookings/",
        json={
            "booking_name": unique_name("booking"),
            "booking_contact_information": "booking@example.com",
            "fees": "false",
            "office_id": seeded_data["office_ids"]["test_office"],
            "room_id": seeded_data["room_id"],
            "start_time": start_time,
            "end_time": end_time,
            "invigilator_id": [seeded_data["invigilator_ids"][0]],
        },
    )
    assert_json_response(response, 201)
    return json_of(response)["booking"]


def test_booking_create_response_matches_the_contract(internal_ga_client, seeded_data):
    """Assert that booking creation returns the stable booking payload contract."""
    start_time, end_time = future_utc_window(2, duration_minutes=120)
    response = internal_ga_client.post(
        "/bookings/",
        json={
            "booking_name": unique_name("booking"),
            "booking_contact_information": "booking@example.com",
            "fees": "false",
            "office_id": seeded_data["office_ids"]["test_office"],
            "room_id": seeded_data["room_id"],
            "start_time": start_time,
            "end_time": end_time,
            "invigilator_id": [seeded_data["invigilator_ids"][0]],
        },
    )
    body = json_of(response)

    assert_json_response(response, 201)
    validate_schema(body, BOOKING_RESPONSE_SCHEMA)
    booking = body["booking"]
    assert booking["invigilators"] == [seeded_data["invigilator_ids"][0]]
    assert booking["local_start_time"] == start_time
    assert booking["local_end_time"] == end_time
    assert booking["start_time"] == local_datetime_to_utc(
        start_time, seeded_data["office_timezones"]["test_office"]
    ).isoformat()
    assert booking["end_time"] == local_datetime_to_utc(
        end_time, seeded_data["office_timezones"]["test_office"]
    ).isoformat()


def test_booking_detail_response_matches_the_contract(internal_ga_client, seeded_data):
    """Assert that booking detail preserves the contract used by booking edit screens."""
    booking = _create_booking(internal_ga_client, seeded_data, days_from_now=2)

    response = internal_ga_client.get(f"/bookings/{booking['booking_id']}/")
    body = json_of(response)

    assert_json_response(response, 200)
    validate_schema(body, BOOKING_RESPONSE_SCHEMA)
    assert body["booking"]["booking_id"] == booking["booking_id"]


def test_booking_list_response_matches_the_contract(internal_ga_client, seeded_data):
    """Assert that booking list items preserve the contract used by booking dashboards."""
    booking = _create_booking(internal_ga_client, seeded_data, days_from_now=2)

    response = internal_ga_client.get("/bookings/")
    body = json_of(response)

    assert_json_response(response, 200)
    validate_schema(body, BOOKING_LIST_RESPONSE_SCHEMA)
    assert any(item["booking_id"] == booking["booking_id"] for item in body["bookings"])
