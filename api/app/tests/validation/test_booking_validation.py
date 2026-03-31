import pytest
from app.tests.api_test_support import assert_json_response, future_utc_window, json_of

pytestmark = [pytest.mark.validation, pytest.mark.usefixtures("seeded_database")]


def test_booking_create_rejects_an_empty_payload(internal_ga_client):
    """Assert that booking creation rejects an empty JSON body with the stable 400 response."""
    response = internal_ga_client.post("/bookings/", json={})

    assert_json_response(response, 400)
    assert json_of(response)["message"] == "No input data received for creating a booking"


def test_booking_create_rejects_a_booking_for_a_different_office(
    internal_ga_client, seeded_data
):
    """Assert that non-designate CSRs cannot create bookings for a different office."""
    start_time, end_time = future_utc_window(2, duration_minutes=120)
    response = internal_ga_client.post(
        "/bookings/",
        json={
            "booking_name": "Wrong office booking",
            "booking_contact_information": "booking@example.com",
            "fees": "false",
            "office_id": seeded_data["office_ids"]["limited_office"],
            "room_id": seeded_data["room_id"],
            "start_time": start_time,
            "end_time": end_time,
            "invigilator_id": [seeded_data["invigilator_ids"][0]],
        },
    )

    assert_json_response(response, 403)
    assert json_of(response)["message"] == (
        "The Booking Office ID and CSR Office ID do not match!"
    )
