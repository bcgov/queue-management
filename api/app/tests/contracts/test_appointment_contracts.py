import pytest
from app.tests.api_test_support import (
    assert_json_response,
    first_day_with_slots,
    future_utc_window,
    json_of,
    slot_window_to_iso,
    unique_name,
)
from app.tests.contracts.conftest import validate_schema
from app.tests.contracts.schemas import (
    APPOINTMENT_LIST_RESPONSE_SCHEMA,
    APPOINTMENT_RESPONSE_SCHEMA,
    SLOTS_SCHEMA,
    USER_APPOINTMENTS_RESPONSE_SCHEMA,
)

pytestmark = [pytest.mark.contracts, pytest.mark.usefixtures("seeded_database")]


def _create_internal_appointment(api_client, seeded_data, *, days_from_now):
    start_time, end_time = future_utc_window(days_from_now)
    response = api_client.post(
        "/appointments/",
        json={
            "service_id": seeded_data["service_ids"]["msp"],
            "office_id": seeded_data["office_ids"]["test_office"],
            "start_time": start_time,
            "end_time": end_time,
            "comments": "Internal appointment",
            "citizen_name": unique_name("internal-appt"),
            "contact_information": "internal@example.com",
        },
    )
    assert_json_response(response, 201)
    return json_of(response)["appointment"]


def test_appointment_create_response_matches_the_contract(
    internal_ga_client, seeded_data
):
    """Assert that appointment creation returns the stable appointment payload contract."""
    start_time, end_time = future_utc_window(2)
    response = internal_ga_client.post(
        "/appointments/",
        json={
            "service_id": seeded_data["service_ids"]["msp"],
            "office_id": seeded_data["office_ids"]["test_office"],
            "start_time": start_time,
            "end_time": end_time,
            "comments": "Internal appointment",
            "citizen_name": unique_name("contract-appt"),
            "contact_information": "internal@example.com",
        },
    )
    body = json_of(response)

    assert_json_response(response, 201)
    validate_schema(body, APPOINTMENT_RESPONSE_SCHEMA)
    assert body["appointment"]["citizen_name"]


def test_appointment_detail_response_matches_the_contract(
    internal_ga_client, seeded_data
):
    """Assert that appointment detail preserves the contract used by appointment edit screens."""
    appointment = _create_internal_appointment(
        internal_ga_client, seeded_data, days_from_now=2
    )

    response = internal_ga_client.get(f"/appointments/{appointment['appointment_id']}/")
    body = json_of(response)

    assert_json_response(response, 200)
    validate_schema(body, APPOINTMENT_RESPONSE_SCHEMA)
    assert body["appointment"]["appointment_id"] == appointment["appointment_id"]


def test_appointment_list_response_matches_the_contract(
    internal_ga_client, seeded_data
):
    """Assert that appointment list items preserve the contract used by calendar views."""
    appointment = _create_internal_appointment(
        internal_ga_client, seeded_data, days_from_now=2
    )

    response = internal_ga_client.get("/appointments/")
    body = json_of(response)

    assert_json_response(response, 200)
    validate_schema(body, APPOINTMENT_LIST_RESPONSE_SCHEMA)
    assert any(
        item["appointment_id"] == appointment["appointment_id"]
        for item in body["appointments"]
    )


def test_slots_response_matches_the_date_keyed_contract(public_client, seeded_data):
    """Assert that public slot availability preserves the date-keyed slot contract."""
    response = public_client.get(
        f"/offices/{seeded_data['office_ids']['limited_office']}/slots/?service_id={seeded_data['service_ids']['limited_office_service']}"
    )
    body = json_of(response)

    assert_json_response(response, 200)
    validate_schema(body, SLOTS_SCHEMA)

    day_key, slots = first_day_with_slots(body)
    assert day_key
    assert slots[0]["no_of_slots"] >= 1


def test_public_user_appointments_response_matches_the_contract(
    public_client, seeded_data
):
    """Assert that public-user appointment listings reuse the stable appointment contract."""
    create_user_response = public_client.post("/users/")
    assert_json_response(create_user_response, 200)

    slots_response = public_client.get(
        f"/offices/{seeded_data['office_ids']['limited_office']}/slots/?service_id={seeded_data['service_ids']['limited_office_service']}"
    )
    assert_json_response(slots_response, 200)

    day_key, slots = first_day_with_slots(json_of(slots_response))
    start_time, end_time = slot_window_to_iso(
        day_key,
        slots[0],
        seeded_data["office_timezones"]["limited_office"],
    )
    create_appointment_response = public_client.post(
        "/appointments/",
        json={
            "service_id": seeded_data["service_ids"]["limited_office_service"],
            "office_id": seeded_data["office_ids"]["limited_office"],
            "start_time": start_time,
            "end_time": end_time,
            "comments": "Public appointment",
            "citizen_name": "Codex Public User",
            "contact_information": "public@example.com",
        },
    )
    assert_json_response(create_appointment_response, 201)

    response = public_client.get("/users/appointments/")
    body = json_of(response)

    assert_json_response(response, 200)
    validate_schema(body, USER_APPOINTMENTS_RESPONSE_SCHEMA)
