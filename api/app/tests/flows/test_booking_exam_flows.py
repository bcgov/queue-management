from __future__ import annotations

from datetime import datetime
from uuid import uuid4
from zoneinfo import ZoneInfo

import pytest
from app.utilities.timezone_utils import local_datetime_to_utc
from app.tests.api_test_support import (
    assert_json_response,
    future_utc_window,
    json_of,
)
from app.tests.api_test_support import (
    create_booking as _create_booking,
)
from app.tests.api_test_support import (
    create_exam as _create_exam,
)

pytestmark = [pytest.mark.flows, pytest.mark.usefixtures("seeded_database")]


def test_booking_can_be_listed_and_retrieved(internal_ga_client, seeded_data):
    """Assert that created bookings appear in list and detail responses."""
    booking = _create_booking(internal_ga_client, seeded_data, days_from_now=2)

    list_response = internal_ga_client.get("/bookings/")
    detail_response = internal_ga_client.get(f"/bookings/{booking['booking_id']}/")

    assert_json_response(list_response, 200)
    assert_json_response(detail_response, 200)
    assert any(
        item["booking_id"] == booking["booking_id"]
        for item in json_of(list_response)["bookings"]
    )
    assert json_of(detail_response)["booking"]["booking_id"] == booking["booking_id"]


def test_booking_can_be_updated(internal_ga_client, seeded_data):
    """Assert that booking updates convert and return office-local times."""
    booking = _create_booking(internal_ga_client, seeded_data, days_from_now=2)
    start_time, end_time = future_utc_window(3, duration_minutes=120)

    response = internal_ga_client.put(
        f"/bookings/{booking['booking_id']}/",
        json={
            "booking_name": "Updated single booking",
            "booking_contact_information": "updated-booking@example.com",
            "invigilator_id": [seeded_data["invigilator_ids"][1]],
            "start_time": start_time,
            "end_time": end_time,
        },
    )

    assert_json_response(response, 200)
    updated = json_of(response)["booking"]
    assert updated["booking_name"] == "Updated single booking"
    assert updated["local_start_time"] == start_time
    assert updated["local_end_time"] == end_time
    assert datetime.fromisoformat(updated["start_time"]) == local_datetime_to_utc(
        start_time, seeded_data["office_timezones"]["test_office"]
    )
    assert datetime.fromisoformat(updated["end_time"]) == local_datetime_to_utc(
        end_time, seeded_data["office_timezones"]["test_office"]
    )


def test_booking_can_be_deleted(internal_ga_client, seeded_data):
    """Assert that bookings can be deleted from the API."""
    booking = _create_booking(internal_ga_client, seeded_data, days_from_now=2)

    response = internal_ga_client.delete(f"/bookings/{booking['booking_id']}/")

    assert response.status_code == 204, response.get_data(as_text=True)


def test_recurring_booking_update_applies_to_each_occurrence(
    internal_ga_client, seeded_data
):
    """Assert that recurring booking updates apply to every matching occurrence."""
    recurring_uuid = str(uuid4())
    first_recurring = _create_booking(
        internal_ga_client,
        seeded_data,
        days_from_now=3,
        recurring_uuid=recurring_uuid,
    )
    second_recurring = _create_booking(
        internal_ga_client,
        seeded_data,
        days_from_now=4,
        recurring_uuid=recurring_uuid,
    )

    recurring_update = internal_ga_client.put(
        f"/bookings/recurring/{recurring_uuid}",
        json={"booking_name": "Recurring booking updated"},
    )
    final_list = internal_ga_client.get("/bookings/")
    bookings = {item["booking_id"]: item for item in json_of(final_list)["bookings"]}

    assert_json_response(recurring_update, 200)
    assert_json_response(final_list, 200)
    assert (
        bookings[first_recurring["booking_id"]]["booking_name"]
        == "Recurring booking updated"
    )
    assert (
        bookings[second_recurring["booking_id"]]["booking_name"]
        == "Recurring booking updated"
    )


def test_recurring_booking_delete_removes_each_occurrence(
    internal_ga_client, seeded_data
):
    """Assert that recurring booking deletion removes every matching occurrence."""
    recurring_uuid = str(uuid4())
    first_recurring = _create_booking(
        internal_ga_client,
        seeded_data,
        days_from_now=3,
        recurring_uuid=recurring_uuid,
    )
    second_recurring = _create_booking(
        internal_ga_client,
        seeded_data,
        days_from_now=4,
        recurring_uuid=recurring_uuid,
    )

    recurring_delete = internal_ga_client.delete(
        f"/bookings/recurring/{recurring_uuid}"
    )
    final_list = internal_ga_client.get("/bookings/")
    final_booking_ids = {item["booking_id"] for item in json_of(final_list)["bookings"]}

    assert recurring_delete.status_code == 204, recurring_delete.get_data(as_text=True)
    assert_json_response(final_list, 200)
    assert first_recurring["booking_id"] not in final_booking_ids
    assert second_recurring["booking_id"] not in final_booking_ids


def test_exam_can_be_listed_and_retrieved(internal_ga_client, seeded_data):
    """Assert that created exams appear in list and detail responses."""
    booking = _create_booking(internal_ga_client, seeded_data, days_from_now=5)
    exam = _create_exam(
        internal_ga_client, seeded_data, booking["booking_id"], event_id="event-detail"
    )

    detail_response = internal_ga_client.get(f"/exams/{exam['exam_id']}/")
    list_response = internal_ga_client.get("/exams/")

    assert_json_response(detail_response, 200)
    assert_json_response(list_response, 200)
    assert json_of(detail_response)["exam"]["exam_id"] == exam["exam_id"]
    assert any(
        item["exam_id"] == exam["exam_id"] for item in json_of(list_response)["exams"]
    )


def test_exam_create_accepts_iso_offset_exam_received_date(
    internal_ga_client, seeded_data
):
    """Assert exam creation accepts frontend ISO offset timestamps."""
    response = internal_ga_client.post(
        "/exams/",
        json={
            "exam_method": "paper",
            "exam_received_date": "2026-04-17T07:00:00+00:00",
            "expiry_date": "2026-05-22T07:00:00+00:00",
            "exam_type_id": seeded_data["exam_type_id"],
            "event_id": "test1234887",
            "exam_name": "test exam",
            "examinee_name": "test candidate",
            "notes": "test notes",
            "office_id": seeded_data["office_ids"]["test_office"],
            "payee_ind": 0,
            "receipt_sent_ind": 0,
            "sbc_managed_ind": 0,
            "exam_returned_ind": 0,
            "exam_written_ind": 0,
            "number_of_students": 1,
        },
    )
    body = json_of(response)

    assert_json_response(response, 201)
    assert body["exam"]["exam_received_date"] == "2026-04-17T07:00:00+00:00"


def test_exam_can_be_updated(internal_ga_client, seeded_data):
    """Assert that exam updates preserve editable exam fields."""
    booking = _create_booking(internal_ga_client, seeded_data, days_from_now=5)
    exam = _create_exam(
        internal_ga_client, seeded_data, booking["booking_id"], event_id="event-update"
    )

    response = internal_ga_client.put(
        f"/exams/{exam['exam_id']}/",
        json={"exam_name": "Updated exam name", "notes": "Updated notes"},
    )

    assert_json_response(response, 201)
    assert json_of(response)["exam"]["exam_name"] == "Updated exam name"


def test_exam_update_accepts_iso_offset_exam_received_date(
    internal_ga_client, seeded_data
):
    """Assert exam updates accept frontend ISO offset timestamps."""
    booking = _create_booking(internal_ga_client, seeded_data, days_from_now=5)
    exam = _create_exam(
        internal_ga_client,
        seeded_data,
        booking["booking_id"],
        event_id="event-upd-recv-date",
    )

    response = internal_ga_client.put(
        f"/exams/{exam['exam_id']}/",
        json={"exam_received_date": "2026-04-17T07:00:00+00:00"},
    )

    assert_json_response(response, 201)
    assert json_of(response)["exam"]["exam_received_date"] == (
        "2026-04-17T07:00:00+00:00"
    )


def test_exam_create_invalid_datetime_returns_validation_response(
    internal_ga_client, seeded_data
):
    """Assert schema load errors return a controlled JSON 422 response."""
    response = internal_ga_client.post(
        "/exams/",
        json={
            "exam_method": "paper",
            "exam_received_date": "not-a-date",
            "expiry_date": "2026-05-22T07:00:00+00:00",
            "exam_type_id": seeded_data["exam_type_id"],
            "event_id": "event-invalid-date",
            "exam_name": "Invalid date exam",
            "examinee_name": "test candidate",
            "notes": "test notes",
            "office_id": seeded_data["office_ids"]["test_office"],
            "payee_ind": 0,
            "receipt_sent_ind": 0,
            "sbc_managed_ind": 0,
            "exam_returned_ind": 0,
            "exam_written_ind": 0,
            "number_of_students": 1,
        },
    )

    assert_json_response(response, 422)
    assert json_of(response) == {
        "message": {"exam_received_date": ["Not a valid datetime."]}
    }


def test_exam_event_lookup_returns_the_matching_exam(internal_ga_client, seeded_data):
    """Assert that exam event lookups continue to find the matching exam."""
    booking = _create_booking(internal_ga_client, seeded_data, days_from_now=5)
    event_id = str(9000 + booking["booking_id"])
    _create_exam(
        internal_ga_client, seeded_data, booking["booking_id"], event_id=event_id
    )

    response = internal_ga_client.get(f"/exams/event_id/{event_id}/")

    assert_json_response(response, 200)
    assert json_of(response)["message"] is True


def test_exam_export_contains_the_updated_exam(internal_ga_client, seeded_data):
    """Assert that exam CSV exports include updated exam data for the requested office day."""
    booking = _create_booking(internal_ga_client, seeded_data, days_from_now=5)
    event_id = str(9000 + booking["booking_id"])
    exam = _create_exam(
        internal_ga_client, seeded_data, booking["booking_id"], event_id=event_id
    )
    update_response = internal_ga_client.put(
        f"/exams/{exam['exam_id']}/",
        json={"exam_name": "Updated exam name", "notes": "Updated notes"},
    )
    assert_json_response(update_response, 201)

    booking_start = datetime.fromisoformat(booking["start_time"].replace("Z", "+00:00"))
    export_date = (
        booking_start.astimezone(
            ZoneInfo(seeded_data["office_timezones"]["test_office"])
        )
        .date()
        .isoformat()
    )
    export_response = internal_ga_client.get(
        f"/exams/export/?start_date={export_date}&end_date={export_date}"
    )

    assert export_response.status_code == 200, export_response.get_data(as_text=True)
    export_body = export_response.get_data(as_text=True)
    assert "Office Name,Exam Type,Exam ID,Exam Name" in export_body
    assert "Updated exam name" in export_body


def test_exam_can_be_deleted(internal_ga_client, seeded_data):
    """Assert that exams can be deleted from the API."""
    booking = _create_booking(internal_ga_client, seeded_data, days_from_now=5)
    exam = _create_exam(
        internal_ga_client, seeded_data, booking["booking_id"], event_id="event-delete"
    )

    delete_response = internal_ga_client.delete(f"/exams/{exam['exam_id']}/")
    post_delete_list = internal_ga_client.get("/exams/")

    assert delete_response.status_code == 204, delete_response.get_data(as_text=True)
    assert_json_response(post_delete_list, 200)
    assert all(
        item["exam_id"] != exam["exam_id"]
        for item in json_of(post_delete_list)["exams"]
    )


def test_invigilator_shadow_count_decrements(internal_ga_client):
    """Assert that subtracting an invigilator shadow count preserves the remaining metadata."""
    list_response = internal_ga_client.get("/invigilators/")
    assert_json_response(list_response, 200)

    first_invigilator = json_of(list_response)["invigilators"][0]
    subtract_response = internal_ga_client.put(
        f"/invigilator/{first_invigilator['invigilator_id']}/?subtract=True&add=False"
    )

    assert_json_response(subtract_response, 200)
    subtracted = json_of(subtract_response)["invigilator"]
    assert subtracted["invigilator_id"] == first_invigilator["invigilator_id"]
    assert subtracted["contact_email"] == first_invigilator["contact_email"]
    assert subtracted["contact_phone"] == first_invigilator["contact_phone"]
    assert subtracted["invigilator_notes"] == first_invigilator["invigilator_notes"]
    assert subtracted["shadow_count"] == 1
    assert subtracted["shadow_flag"] == "N"


def test_invigilator_shadow_count_increment_restores_the_original_value(
    internal_ga_client,
):
    """Assert that adding back a shadow count restores the original invigilator state."""
    list_response = internal_ga_client.get("/invigilators/")
    assert_json_response(list_response, 200)

    first_invigilator = json_of(list_response)["invigilators"][0]
    subtract_response = internal_ga_client.put(
        f"/invigilator/{first_invigilator['invigilator_id']}/?subtract=True&add=False"
    )
    assert_json_response(subtract_response, 200)

    add_response = internal_ga_client.put(
        f"/invigilator/{first_invigilator['invigilator_id']}/?subtract=False&add=True"
    )

    assert_json_response(add_response, 200)
    added_back = json_of(add_response)["invigilator"]
    assert added_back["invigilator_id"] == first_invigilator["invigilator_id"]
    assert added_back["contact_email"] == first_invigilator["contact_email"]
    assert added_back["contact_phone"] == first_invigilator["contact_phone"]
    assert added_back["invigilator_notes"] == first_invigilator["invigilator_notes"]
    assert added_back["shadow_count"] == 2
    assert added_back["shadow_flag"] == "Y"
