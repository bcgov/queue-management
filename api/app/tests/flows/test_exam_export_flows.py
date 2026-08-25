from __future__ import annotations

import csv
import io
from datetime import datetime, timedelta, timezone
from uuid import uuid4
from zoneinfo import ZoneInfo

import pytest
from app.tests.api_test_support import json_of

pytestmark = [pytest.mark.flows, pytest.mark.usefixtures("seeded_database")]


def _set_finance_designate(app, *, username: str, enabled: int):
    with app.app_context():
        from app.models.theq import CSR
        from qsystem import db

        csr = CSR.query.filter_by(username=username).first()
        csr.finance_designate = enabled
        db.session.add(csr)
        db.session.commit()


def _create_export_exam(
    app,
    seeded_data,
    *,
    office_id: int,
    start_time: datetime,
    exam_name: str,
    booking_name: str,
    room_id: int | None = None,
    invigilator_ids: list[int] | None = None,
) -> dict[str, int]:
    with app.app_context():
        from app.models.bookings import Booking, Exam, Invigilator
        from qsystem import db

        booking = Booking(
            office_id=office_id,
            room_id=room_id,
            start_time=start_time,
            end_time=start_time + timedelta(hours=2),
            fees="false",
            booking_name=booking_name,
            booking_contact_information="booking@example.com",
        )
        if invigilator_ids:
            booking.invigilators = (
                Invigilator.query.filter(Invigilator.invigilator_id.in_(invigilator_ids))
                .order_by(Invigilator.invigilator_id)
                .all()
            )
        db.session.add(booking)
        db.session.flush()

        exam = Exam(
            booking_id=booking.booking_id,
            exam_type_id=seeded_data["exam_type_id"],
            office_id=office_id,
            event_id=f"event-{uuid4().hex[:8]}",
            exam_name=exam_name,
            examinee_name="Codex Examinee",
            expiry_date=start_time + timedelta(days=30),
            notes="Export flow",
            number_of_students=1,
            exam_method="paper",
            exam_written_ind=0,
            offsite_location="Test Office",
        )
        db.session.add(exam)
        db.session.commit()
        return {"booking_id": booking.booking_id, "exam_id": exam.exam_id}


def _export_rows(response) -> list[list[str]]:
    return list(csv.reader(io.StringIO(response.get_data(as_text=True))))


def _row_for_exam(rows: list[list[str]], exam_name: str) -> list[str]:
    return next(row for row in rows[1:] if row[3] == exam_name)


def test_exam_export_rejects_missing_or_invalid_dates(internal_ga_client):
    """Assert that export validation fails loudly for missing and malformed date parameters."""
    missing_dates = internal_ga_client.get("/exams/export/?end_date=2024-07-15")
    invalid_dates = internal_ga_client.get(
        "/exams/export/?start_date=2024-13-40&end_date=2024-07-15"
    )

    assert missing_dates.status_code == 422, missing_dates.get_data(as_text=True)
    assert json_of(missing_dates)["message"] == "Must provide both start and end time"

    assert invalid_dates.status_code == 422, invalid_dates.get_data(as_text=True)
    assert json_of(invalid_dates)["message"] == "Unable to return date time string"


def test_exam_export_localizes_times_and_leaves_blank_room_and_invigilator_columns(
    internal_ga_client, seeded_data, app
):
    """Assert that CSV rows keep localized timestamps while tolerating bookings without room or invigilator data."""
    start_time = datetime(2024, 7, 15, 17, 0, tzinfo=timezone.utc)
    _create_export_exam(
        app,
        seeded_data,
        office_id=seeded_data["office_ids"]["test_office"],
        start_time=start_time,
        exam_name="No Room Exam",
        booking_name="No Room Booking",
        room_id=None,
        invigilator_ids=[],
    )

    export_date = (
        start_time.astimezone(
            ZoneInfo(seeded_data["office_timezones"]["test_office"])
        )
        .date()
        .isoformat()
    )
    response = internal_ga_client.get(
        f"/exams/export/?start_date={export_date}&end_date={export_date}"
    )

    assert response.status_code == 200, response.get_data(as_text=True)
    row = _row_for_exam(_export_rows(response), "No Room Exam")

    expected_start = start_time.astimezone(
        ZoneInfo(seeded_data["office_timezones"]["test_office"])
    ).strftime("%Y-%m-%d %I:%M %p")
    expected_end = (start_time + timedelta(hours=2)).astimezone(
        ZoneInfo(seeded_data["office_timezones"]["test_office"])
    ).strftime("%Y-%m-%d %I:%M %p")

    assert row[6] == ""
    assert row[7] == ""
    assert row[10] == f'="{expected_start}"'
    assert row[11] == f'="{expected_end}"'


def test_exam_export_limits_non_designates_to_their_own_office_but_allows_designates_to_export_all_offices(
    internal_ga_client, internal_nonqtxn_client, seeded_data, app
):
    """Assert that finance designates can export rows from other offices while non-designates stay office-scoped."""
    start_time = datetime(2024, 7, 20, 17, 0, tzinfo=timezone.utc)
    _create_export_exam(
        app,
        seeded_data,
        office_id=seeded_data["office_ids"]["victoria"],
        start_time=start_time,
        exam_name="Victoria Export Exam",
        booking_name="Victoria Export Booking",
    )
    export_date = (
        start_time.astimezone(ZoneInfo(seeded_data["office_timezones"]["victoria"]))
        .date()
        .isoformat()
    )

    _set_finance_designate(app, username="cfms-postman-operator", enabled=0)
    non_designate_response = internal_ga_client.get(
        f"/exams/export/?start_date={export_date}&end_date={export_date}"
    )

    assert non_designate_response.status_code == 200, non_designate_response.get_data(
        as_text=True
    )
    non_designate_exam_names = {row[3] for row in _export_rows(non_designate_response)[1:]}
    assert "Victoria Export Exam" not in non_designate_exam_names

    _set_finance_designate(app, username="cfms-postman-non-operator", enabled=1)
    designate_response = internal_nonqtxn_client.get(
        f"/exams/export/?start_date={export_date}&end_date={export_date}"
    )

    assert designate_response.status_code == 200, designate_response.get_data(as_text=True)
    designate_exam_names = {row[3] for row in _export_rows(designate_response)[1:]}
    assert "Victoria Export Exam" in designate_exam_names
