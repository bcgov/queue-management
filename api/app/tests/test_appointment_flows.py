from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Optional
from uuid import uuid4

import pytest

from app.tests.api_test_support import (
    assert_status,
    first_day_with_slots,
    json_of,
    slot_window_to_iso,
    unique_name,
)


pytestmark = [pytest.mark.flows, pytest.mark.usefixtures("seeded_database")]


def _future_window(days_from_now: int, duration_minutes: int = 30) -> tuple[str, str]:
    start = datetime.now(timezone.utc).replace(microsecond=0, second=0, minute=0) + timedelta(days=days_from_now)
    end = start + timedelta(minutes=duration_minutes)
    return start.isoformat(), end.isoformat()


def _create_internal_appointment(api_client, seeded_data, *, days_from_now: int, recurring_uuid: Optional[str] = None):
    start_time, end_time = _future_window(days_from_now)
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
            "recurring_uuid": recurring_uuid,
        },
    )
    assert_status(response, 201)
    return json_of(response)["appointment"]


def _public_slot_payload(public_client, seeded_data, *, minimum_slots: int = 1):
    slots_response = public_client.get(
        f"/offices/{seeded_data['office_ids']['limited_office']}/slots/?service_id={seeded_data['service_ids']['limited_office_service']}"
    )
    assert_status(slots_response, 200)
    day_key, slots = first_day_with_slots(json_of(slots_response), minimum_slots=minimum_slots)
    start_time, end_time = slot_window_to_iso(day_key, slots[0], seeded_data["office_timezones"]["limited_office"])
    return {
        "service_id": seeded_data["service_ids"]["limited_office_service"],
        "office_id": seeded_data["office_ids"]["limited_office"],
        "start_time": start_time,
        "end_time": end_time,
        "comments": "Public appointment",
        "citizen_name": "Codex Public User",
        "contact_information": "public@example.com",
    }, day_key, slots


def test_internal_appointment_crud_and_recurring_workflows(internal_ga_client, seeded_data):
    appointment = _create_internal_appointment(internal_ga_client, seeded_data, days_from_now=2)

    list_response = internal_ga_client.get("/appointments/")
    detail_response = internal_ga_client.get(f"/appointments/{appointment['appointment_id']}/")
    update_response = internal_ga_client.put(
        f"/appointments/{appointment['appointment_id']}/",
        json={"comments": "Internal appointment updated"},
    )
    delete_response = internal_ga_client.delete(f"/appointments/{appointment['appointment_id']}/")

    assert_status(list_response, 200)
    assert_status(detail_response, 200)
    assert_status(update_response, 200)
    assert_status(delete_response, 204)
    assert any(item["appointment_id"] == appointment["appointment_id"] for item in json_of(list_response)["appointments"])
    assert json_of(update_response)["appointment"]["comments"] == "Internal appointment updated"

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
    recurring_delete = internal_ga_client.delete(f"/appointments/recurring/{recurring_uuid}")
    final_list = internal_ga_client.get("/appointments/")

    assert_status(recurring_update, 200)
    assert_status(recurring_delete, 204)
    assert_status(final_list, 200)
    remaining_ids = {item["appointment_id"] for item in json_of(final_list)["appointments"]}
    assert first_recurring["appointment_id"] not in remaining_ids
    assert second_recurring["appointment_id"] not in remaining_ids


def test_public_user_profile_and_appointment_workflows(public_client, seeded_data):
    create_user_response = public_client.post("/users/")
    assert_status(create_user_response, 200)
    created_user = json_of(create_user_response)[0]

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

    assert_status(update_user_response, 200)
    assert_status(get_me_response, 200)
    assert json_of(update_user_response)[0]["email"] == "updated-public@example.com"

    appointment_payload, day_key, slots = _public_slot_payload(public_client, seeded_data, minimum_slots=2)
    create_appointment_response = public_client.post("/appointments/", json=appointment_payload)
    assert_status(create_appointment_response, 201)
    appointment = json_of(create_appointment_response)["appointment"]

    list_response = public_client.get("/users/appointments/")
    assert_status(list_response, 200)
    assert any(item["appointment_id"] == appointment["appointment_id"] for item in json_of(list_response)["appointments"])

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
    assert_status(max_limit_response, 400)
    assert json_of(max_limit_response)["code"] == "MAX_NO_OF_APPOINTMENTS_REACHED"

    delete_response = public_client.delete(f"/appointments/{appointment['appointment_id']}/")
    assert_status(delete_response, 204)


def test_appointment_slots_endpoint(public_client, seeded_data):
    response = public_client.get(
        f"/offices/{seeded_data['office_ids']['limited_office']}/slots/?service_id={seeded_data['service_ids']['limited_office_service']}"
    )

    assert_status(response, 200)
    day_key, slots = first_day_with_slots(json_of(response))
    assert day_key
    assert slots[0]["no_of_slots"] >= 1
