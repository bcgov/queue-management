from datetime import datetime, timedelta, timezone

import pytest
from app.tests.api_test_support import (
    assert_json_response,
    future_utc_window,
    json_of,
    unique_name,
)
from app.tests.contracts.conftest import validate_schema
from app.tests.contracts.schemas import EXAM_LIST_RESPONSE_SCHEMA, EXAM_RESPONSE_SCHEMA

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


def _create_exam(api_client, seeded_data, booking_id, *, event_id):
    expiry_date = (
        (datetime.now(timezone.utc) + timedelta(days=30))
        .replace(microsecond=0)
        .isoformat()
    )
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
    assert_json_response(response, 201)
    return json_of(response)["exam"]


def test_exam_create_response_matches_the_contract(internal_ga_client, seeded_data):
    """Assert that exam creation returns the stable exam payload contract."""
    booking = _create_booking(internal_ga_client, seeded_data, days_from_now=5)
    response = internal_ga_client.post(
        "/exams/",
        json={
            "booking_id": booking["booking_id"],
            "event_id": f"event-{booking['booking_id']}",
            "exam_method": "paper",
            "exam_name": unique_name("exam"),
            "exam_type_id": seeded_data["exam_type_id"],
            "exam_written_ind": 0,
            "examinee_name": "Codex Examinee",
            "notes": "Codex exam notes",
            "number_of_students": 19,
            "office_id": seeded_data["office_ids"]["test_office"],
            "offsite_location": "Test Office",
            "expiry_date": (datetime.now(timezone.utc) + timedelta(days=30))
            .replace(microsecond=0)
            .isoformat(),
        },
    )
    body = json_of(response)

    assert_json_response(response, 201)
    validate_schema(body, EXAM_RESPONSE_SCHEMA)
    assert body["exam"]["booking_id"] == booking["booking_id"]


def test_exam_detail_response_matches_the_contract(internal_ga_client, seeded_data):
    """Assert that exam detail preserves the contract used by exam detail screens."""
    booking = _create_booking(internal_ga_client, seeded_data, days_from_now=5)
    exam = _create_exam(
        internal_ga_client, seeded_data, booking["booking_id"], event_id="event-detail"
    )

    response = internal_ga_client.get(f"/exams/{exam['exam_id']}/")
    body = json_of(response)

    assert_json_response(response, 200)
    validate_schema(body, EXAM_RESPONSE_SCHEMA)
    assert body["exam"]["exam_id"] == exam["exam_id"]


def test_exam_list_response_matches_the_contract(internal_ga_client, seeded_data):
    """Assert that exam list items preserve the contract used by exam dashboards."""
    booking = _create_booking(internal_ga_client, seeded_data, days_from_now=5)
    exam = _create_exam(
        internal_ga_client, seeded_data, booking["booking_id"], event_id="event-list"
    )

    response = internal_ga_client.get("/exams/")
    body = json_of(response)

    assert_json_response(response, 200)
    validate_schema(body, EXAM_LIST_RESPONSE_SCHEMA)
    assert any(item["exam_id"] == exam["exam_id"] for item in body["exams"])
