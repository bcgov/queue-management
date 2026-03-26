from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Optional
from uuid import uuid4
from zoneinfo import ZoneInfo

import pytest

from app.tests.api_test_support import assert_status, json_of, unique_name


pytestmark = [pytest.mark.flows, pytest.mark.usefixtures("seeded_database")]


def _future_window(days_from_now: int, duration_hours: int = 2) -> tuple[str, str]:
    start = datetime.now(timezone.utc).replace(microsecond=0, second=0, minute=0) + timedelta(days=days_from_now)
    end = start + timedelta(hours=duration_hours)
    return start.isoformat(), end.isoformat()


def _create_booking(api_client, seeded_data, *, days_from_now: int, recurring_uuid: Optional[str] = None):
    start_time, end_time = _future_window(days_from_now)
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
            "recurring_uuid": recurring_uuid,
            "invigilator_id": [seeded_data["invigilator_ids"][0]],
        },
    )
    assert_status(response, 201)
    return json_of(response)["booking"]


def _create_exam(api_client, seeded_data, booking_id: int, *, event_id: str):
    expiry_date = (datetime.now(timezone.utc) + timedelta(days=30)).replace(microsecond=0).isoformat()
    response = api_client.post(
        "/exams/",
        json={
            "booking_id": booking_id,
            "event_id": event_id,
            "exam_method": "paper",
            "exam_name": unique_name("exam"),
            "exam_type_id": seeded_data["exam_type_id"],
            "exam_written_ind": 0,
            "examinee_name": "Codex Examinee",
            "notes": "Codex exam notes",
            "number_of_students": 19,
            "office_id": seeded_data["office_ids"]["test_office"],
            "offsite_location": "Test Office",
            "expiry_date": expiry_date,
        },
    )
    assert_status(response, 201)
    return json_of(response)["exam"]


def test_booking_crud_and_recurring_workflows(internal_ga_client, seeded_data):
    booking = _create_booking(internal_ga_client, seeded_data, days_from_now=2)

    list_response = internal_ga_client.get("/bookings/")
    detail_response = internal_ga_client.get(f"/bookings/{booking['booking_id']}/")
    update_response = internal_ga_client.put(
        f"/bookings/{booking['booking_id']}/",
        json={
            "booking_name": "Updated single booking",
            "booking_contact_information": "updated-booking@example.com",
            "invigilator_id": [seeded_data["invigilator_ids"][1]],
        },
    )
    delete_response = internal_ga_client.delete(f"/bookings/{booking['booking_id']}/")

    assert_status(list_response, 200)
    assert_status(detail_response, 200)
    assert_status(update_response, 200)
    assert_status(delete_response, 204)
    assert any(item["booking_id"] == booking["booking_id"] for item in json_of(list_response)["bookings"])
    assert json_of(update_response)["booking"]["booking_name"] == "Updated single booking"

    recurring_uuid = str(uuid4())
    first_recurring = _create_booking(internal_ga_client, seeded_data, days_from_now=3, recurring_uuid=recurring_uuid)
    second_recurring = _create_booking(internal_ga_client, seeded_data, days_from_now=4, recurring_uuid=recurring_uuid)

    recurring_update = internal_ga_client.put(
        f"/bookings/recurring/{recurring_uuid}",
        json={"booking_name": "Recurring booking updated"},
    )
    recurring_delete = internal_ga_client.delete(f"/bookings/recurring/{recurring_uuid}")
    final_list = internal_ga_client.get("/bookings/")

    assert_status(recurring_update, 200)
    assert_status(recurring_delete, 204)
    assert_status(final_list, 200)
    final_booking_ids = {item["booking_id"] for item in json_of(final_list)["bookings"]}
    assert first_recurring["booking_id"] not in final_booking_ids
    assert second_recurring["booking_id"] not in final_booking_ids


def test_exam_crud_event_lookup_and_export(internal_ga_client, seeded_data):
    booking = _create_booking(internal_ga_client, seeded_data, days_from_now=5)
    event_id = str(9000 + booking["booking_id"])
    exam = _create_exam(internal_ga_client, seeded_data, booking["booking_id"], event_id=event_id)

    detail_response = internal_ga_client.get(f"/exams/{exam['exam_id']}/")
    list_response = internal_ga_client.get("/exams/")
    update_response = internal_ga_client.put(
        f"/exams/{exam['exam_id']}/",
        json={"exam_name": "Updated exam name", "notes": "Updated notes"},
    )
    event_lookup_response = internal_ga_client.get(f"/exams/event_id/{event_id}/")

    booking_start = datetime.fromisoformat(booking["start_time"].replace("Z", "+00:00"))
    export_date = booking_start.astimezone(
        ZoneInfo(seeded_data["office_timezones"]["test_office"])
    ).date().isoformat()
    export_response = internal_ga_client.get(f"/exams/export/?start_date={export_date}&end_date={export_date}")
    delete_response = internal_ga_client.delete(f"/exams/{exam['exam_id']}/")
    post_delete_list = internal_ga_client.get("/exams/")

    assert_status(detail_response, 200)
    assert_status(list_response, 200)
    assert_status(update_response, 201)
    assert_status(event_lookup_response, 200)
    assert_status(export_response, 200)
    assert_status(delete_response, 204)
    assert_status(post_delete_list, 200)

    assert json_of(detail_response)["exam"]["event_id"] == event_id
    assert any(item["exam_id"] == exam["exam_id"] for item in json_of(list_response)["exams"])
    assert json_of(update_response)["exam"]["exam_name"] == "Updated exam name"
    assert json_of(event_lookup_response)["message"] is True
    export_body = export_response.get_data(as_text=True)
    assert "Office Name,Exam Type,Exam ID,Exam Name" in export_body
    assert "Updated exam name" in export_body
    assert all(item["exam_id"] != exam["exam_id"] for item in json_of(post_delete_list)["exams"])


def test_invigilator_lists_and_shadow_count_mutations(internal_ga_client):
    list_response = internal_ga_client.get("/invigilators/")
    offsite_response = internal_ga_client.get("/invigilators/offsite/")

    assert_status(list_response, 200)
    assert_status(offsite_response, 200)

    invigilators = json_of(list_response)["invigilators"]
    offsite_invigilators = json_of(offsite_response)["invigilators"]

    assert invigilators
    assert offsite_invigilators

    first_invigilator = invigilators[0]
    assert first_invigilator["shadow_count"] == 2
    assert first_invigilator["shadow_flag"] == "Y"
    assert any(
        invigilator["invigilator_name"] == "Pest 1" for invigilator in offsite_invigilators
    )

    subtract_response = internal_ga_client.put(
        f"/invigilator/{first_invigilator['invigilator_id']}/?subtract=True&add=False"
    )
    assert_status(subtract_response, 200)
    subtracted = json_of(subtract_response)["invigilator"]

    assert subtracted["invigilator_id"] == first_invigilator["invigilator_id"]
    assert subtracted["contact_email"] == first_invigilator["contact_email"]
    assert subtracted["contact_phone"] == first_invigilator["contact_phone"]
    assert subtracted["invigilator_notes"] == first_invigilator["invigilator_notes"]
    assert subtracted["shadow_count"] == 1
    assert subtracted["shadow_flag"] == "N"

    add_response = internal_ga_client.put(
        f"/invigilator/{first_invigilator['invigilator_id']}/?subtract=False&add=True"
    )
    assert_status(add_response, 200)
    added_back = json_of(add_response)["invigilator"]

    assert added_back["invigilator_id"] == first_invigilator["invigilator_id"]
    assert added_back["contact_email"] == first_invigilator["contact_email"]
    assert added_back["contact_phone"] == first_invigilator["contact_phone"]
    assert added_back["invigilator_notes"] == first_invigilator["invigilator_notes"]
    assert added_back["shadow_count"] == 2
    assert added_back["shadow_flag"] == "Y"
