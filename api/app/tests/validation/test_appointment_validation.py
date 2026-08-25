from __future__ import annotations

import pytest
from app.tests.api_test_support import (
    assert_json_response,
    create_public_user,
    future_utc_window,
    json_of,
    public_slot_payload,
    slot_window_to_iso,
    unique_name,
)

pytestmark = [pytest.mark.validation, pytest.mark.usefixtures("seeded_database")]


def test_anonymous_draft_create_rejects_a_conflicting_slot(bare_client, seeded_data):
    """Assert that anonymous draft creation returns CONFLICT_APPOINTMENT when the slot is already reserved."""
    payload, _day_key, _slots = public_slot_payload(
        bare_client, seeded_data, minimum_slots=1
    )
    assert_json_response(bare_client.post("/appointments/draft", json=payload), 201)

    response = bare_client.post("/appointments/draft", json=payload)

    assert_json_response(response, 400)
    assert json_of(response)["code"] == "CONFLICT_APPOINTMENT"


def test_public_appointment_create_rejects_a_conflict_across_different_users(
    public_client, public_client_alt, seeded_data
):
    """Assert that one public user's appointment blocks a different public user from taking the same slot."""
    create_public_user(public_client)
    create_public_user(public_client_alt)
    payload, _day_key, _slots = public_slot_payload(
        public_client, seeded_data, minimum_slots=1
    )
    assert_json_response(public_client.post("/appointments/", json=payload), 201)

    response = public_client_alt.post("/appointments/", json=payload)

    assert_json_response(response, 400)
    assert json_of(response)["code"] == "CONFLICT_APPOINTMENT"


def test_public_appointment_update_rejects_moving_onto_another_users_slot(
    public_client, public_client_alt, seeded_data
):
    """Assert that updating a public appointment into another user's booked slot returns CONFLICT_APPOINTMENT."""
    create_public_user(public_client)
    payload, day_key, slots = public_slot_payload(
        public_client, seeded_data, minimum_slots=2
    )
    first_response = public_client.post("/appointments/", json=payload)
    assert_json_response(first_response, 201)
    taken_appointment = json_of(first_response)["appointment"]

    create_public_user(public_client_alt)
    other_start_time, other_end_time = slot_window_to_iso(
        day_key,
        slots[1],
        seeded_data["office_timezones"]["limited_office"],
    )
    second_response = public_client_alt.post(
        "/appointments/",
        json={
            **payload,
            "start_time": other_start_time,
            "end_time": other_end_time,
        },
    )
    assert_json_response(second_response, 201)
    other_appointment = json_of(second_response)["appointment"]

    response = public_client_alt.put(
        f"/appointments/{other_appointment['appointment_id']}/",
        json={
            "comments": "Move into a conflicting slot",
            "office_id": other_appointment["office_id"],
            "service_id": other_appointment["service_id"],
            "start_time": taken_appointment["start_time"],
            "end_time": taken_appointment["end_time"],
        },
    )

    assert_json_response(response, 400)
    assert json_of(response)["code"] == "CONFLICT_APPOINTMENT"


def test_public_user_cannot_update_another_users_appointment(
    public_client, public_client_alt, seeded_data
):
    """Assert that a public user receives 403 when attempting to update another public user's appointment."""
    create_public_user(public_client)
    payload, day_key, slots = public_slot_payload(
        public_client, seeded_data, minimum_slots=2
    )
    first_response = public_client.post("/appointments/", json=payload)
    assert_json_response(first_response, 201)
    appointment = json_of(first_response)["appointment"]

    create_public_user(public_client_alt)
    alternate_start_time, alternate_end_time = slot_window_to_iso(
        day_key,
        slots[1],
        seeded_data["office_timezones"]["limited_office"],
    )
    response = public_client_alt.put(
        f"/appointments/{appointment['appointment_id']}/",
        json={
            "comments": "Attempted cross-user update",
            "office_id": appointment["office_id"],
            "service_id": appointment["service_id"],
            "start_time": alternate_start_time,
            "end_time": alternate_end_time,
        },
    )

    assert response.status_code == 403, response.get_data(as_text=True)


def test_public_user_create_rejects_when_the_daily_limit_is_reached(
    public_client, seeded_data
):
    """Assert that the public appointment create route freezes the daily booking limit error contract."""
    create_public_user(public_client)
    payload, day_key, slots = public_slot_payload(
        public_client, seeded_data, minimum_slots=2
    )
    first_response = public_client.post("/appointments/", json=payload)
    assert_json_response(first_response, 201)

    alternate_start_time, alternate_end_time = slot_window_to_iso(
        day_key,
        slots[1],
        seeded_data["office_timezones"]["limited_office"],
    )
    response = public_client.post(
        "/appointments/",
        json={
            **payload,
            "start_time": alternate_start_time,
            "end_time": alternate_end_time,
        },
    )

    assert_json_response(response, 400)
    assert json_of(response) == {
        "code": "MAX_NO_OF_APPOINTMENTS_REACHED",
        "message": "Maximum number of appointments reached",
    }


def test_internal_appointment_create_rejects_unknown_service_id(
    internal_ga_client, seeded_data
):
    """Assert that internal appointment creation returns JSON 400 for invalid service ids."""
    start_time, end_time = future_utc_window(2)
    response = internal_ga_client.post(
        "/appointments/",
        json={
            "service_id": 999999,
            "office_id": seeded_data["office_ids"]["test_office"],
            "start_time": start_time,
            "end_time": end_time,
            "comments": "Internal invalid service",
            "citizen_name": unique_name("invalid-service"),
            "contact_information": "internal@example.com",
        },
    )

    assert_json_response(response, 400)
    assert json_of(response)["message"] == "Could not find service for service_id: 999999"


def test_internal_appointment_create_rejects_mismatched_office_as_json(
    internal_ga_client, seeded_data
):
    """Assert that internal appointment creation returns a JSON 403 when the payload office differs from the CSR office."""
    start_time, end_time = future_utc_window(2)
    response = internal_ga_client.post(
        "/appointments/",
        json={
            "service_id": seeded_data["service_ids"]["msp"],
            "office_id": seeded_data["office_ids"]["limited_office"],
            "start_time": start_time,
            "end_time": end_time,
            "comments": "Internal mismatched office",
            "citizen_name": unique_name("mismatched-office"),
            "contact_information": "internal@example.com",
        },
    )

    assert_json_response(response, 403)
    assert (
        json_of(response)["message"]
        == "The Appointment Office ID and CSR Office ID do not match!"
    )


def test_public_appointment_create_rejects_unknown_service_id(
    public_client, seeded_data
):
    """Assert that public appointment creation returns JSON 400 for invalid service ids."""
    create_public_user(public_client)
    payload, _day_key, _slots = public_slot_payload(
        public_client, seeded_data, minimum_slots=1
    )
    response = public_client.post(
        "/appointments/",
        json={**payload, "service_id": 999999},
    )

    assert_json_response(response, 400)
    assert json_of(response)["message"] == "Could not find service for service_id: 999999"
