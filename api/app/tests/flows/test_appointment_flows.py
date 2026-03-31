from __future__ import annotations

from uuid import uuid4

import pytest
from app.tests.api_test_support import (
    assert_json_response,
    create_public_user,
    first_day_with_slots,
    json_of,
    public_slot_payload,
    slot_window_to_iso,
)
from app.tests.api_test_support import (
    create_internal_appointment as _create_internal_appointment,
)

pytestmark = [pytest.mark.flows, pytest.mark.usefixtures("seeded_database")]


def test_internal_appointment_can_be_listed_and_retrieved(
    internal_ga_client, seeded_data
):
    """Assert that created internal appointments appear in list and detail responses."""
    appointment = _create_internal_appointment(
        internal_ga_client, seeded_data, days_from_now=2
    )

    list_response = internal_ga_client.get("/appointments/")
    detail_response = internal_ga_client.get(
        f"/appointments/{appointment['appointment_id']}/"
    )

    assert_json_response(list_response, 200)
    assert_json_response(detail_response, 200)
    assert any(
        item["appointment_id"] == appointment["appointment_id"]
        for item in json_of(list_response)["appointments"]
    )
    assert (
        json_of(detail_response)["appointment"]["appointment_id"]
        == appointment["appointment_id"]
    )


def test_internal_appointment_can_be_updated(internal_ga_client, seeded_data):
    """Assert that internal appointments preserve comment updates."""
    appointment = _create_internal_appointment(
        internal_ga_client, seeded_data, days_from_now=2
    )

    response = internal_ga_client.put(
        f"/appointments/{appointment['appointment_id']}/",
        json={"comments": "Internal appointment updated"},
    )

    assert_json_response(response, 200)
    assert (
        json_of(response)["appointment"]["comments"] == "Internal appointment updated"
    )


def test_internal_appointment_can_be_deleted(internal_ga_client, seeded_data):
    """Assert that internal appointments can be deleted from the API."""
    appointment = _create_internal_appointment(
        internal_ga_client, seeded_data, days_from_now=2
    )

    response = internal_ga_client.delete(
        f"/appointments/{appointment['appointment_id']}/"
    )

    assert response.status_code == 204, response.get_data(as_text=True)


def test_recurring_appointment_update_applies_to_each_occurrence(
    internal_ga_client, seeded_data
):
    """Assert that recurring appointment updates apply across all matching occurrences."""
    recurring_uuid = str(uuid4())
    first_recurring = _create_internal_appointment(
        internal_ga_client,
        seeded_data,
        days_from_now=3,
        recurring_uuid=recurring_uuid,
    )
    second_recurring = _create_internal_appointment(
        internal_ga_client,
        seeded_data,
        days_from_now=4,
        recurring_uuid=recurring_uuid,
    )

    recurring_update = internal_ga_client.put(
        f"/appointments/recurring/{recurring_uuid}",
        json={"comments": "Recurring appointment updated"},
    )
    final_list = internal_ga_client.get("/appointments/")
    appointments = {
        item["appointment_id"]: item for item in json_of(final_list)["appointments"]
    }

    assert_json_response(recurring_update, 200)
    assert_json_response(final_list, 200)
    assert (
        appointments[first_recurring["appointment_id"]]["comments"]
        == "Recurring appointment updated"
    )
    assert (
        appointments[second_recurring["appointment_id"]]["comments"]
        == "Recurring appointment updated"
    )


def test_recurring_appointment_delete_removes_each_occurrence(
    internal_ga_client, seeded_data
):
    """Assert that recurring appointment deletion removes every matching occurrence."""
    recurring_uuid = str(uuid4())
    first_recurring = _create_internal_appointment(
        internal_ga_client,
        seeded_data,
        days_from_now=3,
        recurring_uuid=recurring_uuid,
    )
    second_recurring = _create_internal_appointment(
        internal_ga_client,
        seeded_data,
        days_from_now=4,
        recurring_uuid=recurring_uuid,
    )

    recurring_delete = internal_ga_client.delete(
        f"/appointments/recurring/{recurring_uuid}"
    )
    final_list = internal_ga_client.get("/appointments/")
    remaining_ids = {
        item["appointment_id"] for item in json_of(final_list)["appointments"]
    }

    assert recurring_delete.status_code == 204, recurring_delete.get_data(as_text=True)
    assert_json_response(final_list, 200)
    assert first_recurring["appointment_id"] not in remaining_ids
    assert second_recurring["appointment_id"] not in remaining_ids


def test_public_user_profile_can_be_created_and_updated(public_client):
    """Assert that public-user profiles can be created and updated before booking."""
    created_user = create_public_user(public_client)

    update_user_response = public_client.put(
        f"/users/{created_user['user_id']}/",
        json={
            "email": "updated-public@example.com",
            "telephone": "2505550100",
            "send_email_reminders": True,
            "send_sms_reminders": True,
        },
    )
    get_me_response = public_client.get("/users/me/")

    assert_json_response(update_user_response, 200)
    assert_json_response(get_me_response, 200)
    assert json_of(update_user_response)[0]["email"] == "updated-public@example.com"


def test_public_user_appointment_appears_in_their_appointment_list(
    public_client, seeded_data
):
    """Assert that public bookings appear in the authenticated user's appointment list."""
    create_public_user(public_client)

    appointment_payload, _day_key, _slots = public_slot_payload(
        public_client, seeded_data, minimum_slots=2
    )
    create_appointment_response = public_client.post(
        "/appointments/", json=appointment_payload
    )
    assert_json_response(create_appointment_response, 201)
    appointment = json_of(create_appointment_response)["appointment"]

    list_response = public_client.get("/users/appointments/")

    assert_json_response(list_response, 200)
    assert any(
        item["appointment_id"] == appointment["appointment_id"]
        for item in json_of(list_response)["appointments"]
    )


def test_public_user_appointment_limit_rejects_a_second_booking(
    public_client, seeded_data
):
    """Assert that the public appointment limit rejects a second booking on the same day."""
    create_public_user(public_client)

    appointment_payload, day_key, slots = public_slot_payload(
        public_client, seeded_data, minimum_slots=2
    )
    first_response = public_client.post("/appointments/", json=appointment_payload)
    assert_json_response(first_response, 201)

    second_start_time, second_end_time = slot_window_to_iso(
        day_key,
        slots[1],
        seeded_data["office_timezones"]["limited_office"],
    )
    max_limit_response = public_client.post(
        "/appointments/",
        json={
            **appointment_payload,
            "start_time": second_start_time,
            "end_time": second_end_time,
        },
    )

    assert_json_response(max_limit_response, 400)
    assert json_of(max_limit_response)["code"] == "MAX_NO_OF_APPOINTMENTS_REACHED"


def test_public_user_can_cancel_their_appointment(public_client, seeded_data):
    """Assert that public users can cancel their own appointment bookings."""
    create_public_user(public_client)

    appointment_payload, _day_key, _slots = public_slot_payload(
        public_client, seeded_data, minimum_slots=1
    )
    create_appointment_response = public_client.post(
        "/appointments/", json=appointment_payload
    )
    assert_json_response(create_appointment_response, 201)
    appointment = json_of(create_appointment_response)["appointment"]

    delete_response = public_client.delete(
        f"/appointments/{appointment['appointment_id']}/"
    )

    assert delete_response.status_code == 204, delete_response.get_data(as_text=True)


def test_appointment_slots_endpoint_returns_available_capacity(
    public_client, seeded_data
):
    """Assert that the slots endpoint exposes at least one available slot with capacity metadata."""
    response = public_client.get(
        f"/offices/{seeded_data['office_ids']['limited_office']}/slots/?service_id={seeded_data['service_ids']['limited_office_service']}"
    )

    assert_json_response(response, 200)
    day_key, slots = first_day_with_slots(json_of(response))
    assert day_key
    assert slots[0]["no_of_slots"] >= 1
