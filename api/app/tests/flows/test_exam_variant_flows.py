from __future__ import annotations

import csv
import io
from datetime import datetime
from uuid import uuid4
from zoneinfo import ZoneInfo

import pytest
from app.tests.api_test_support import (
    assert_json_response,
    create_booking,
    create_exam,
    json_of,
)

pytestmark = [pytest.mark.flows, pytest.mark.usefixtures("seeded_database")]


def _exam_type_id(
    app,
    *,
    exam_type_name: str | None = None,
    group_exam_ind: int | None = None,
    ita_ind: int | None = None,
    pesticide_exam_ind: int | None = None,
) -> int:
    with app.app_context():
        from app.models.bookings import ExamType

        query = ExamType.query
        if exam_type_name is not None:
            query = query.filter_by(exam_type_name=exam_type_name)
        if group_exam_ind is not None:
            query = query.filter_by(group_exam_ind=group_exam_ind)
        if ita_ind is not None:
            query = query.filter_by(ita_ind=ita_ind)
        if pesticide_exam_ind is not None:
            query = query.filter_by(pesticide_exam_ind=pesticide_exam_ind)

        exam_type = query.order_by(ExamType.exam_type_id).first()
        assert exam_type is not None
        return exam_type.exam_type_id


def _pesticide_office_id(app) -> int:
    with app.app_context():
        from app.models.theq import Office

        office = Office.query.filter_by(office_name="Pesticide Offsite").first()
        assert office is not None
        return office.office_id


def _export_date(booking: dict, timezone_name: str) -> str:
    booking_start = datetime.fromisoformat(booking["start_time"].replace("Z", "+00:00"))
    return booking_start.astimezone(ZoneInfo(timezone_name)).date().isoformat()


def test_pesticide_individual_exam_preserves_type_and_sets_job_event_id(
    app, monkeypatch, internal_ga_client, seeded_data
):
    """Assert that pesticide individual exam creation keeps the chosen type and maps BCMP job ids to event ids."""
    from app.resources.bookings.exam.exam_post import ExamPost

    exam_type_id = _exam_type_id(
        app, group_exam_ind=0, ita_ind=0, pesticide_exam_ind=1
    )
    monkeypatch.setattr(
        ExamPost.bcmp_service,
        "check_exam_status",
        lambda exam: {"jobProperties": {"JOB_ID": f"job-{exam.exam_name}"}},
    )

    response = internal_ga_client.post(
        "/exams/",
        json={
            "event_id": "placeholder",
            "exam_method": "paper",
            "exam_name": "Pesticide Individual",
            "exam_type_id": exam_type_id,
            "exam_written_ind": 0,
            "examinee_name": "Codex Examinee",
            "notes": "Pesticide individual flow",
            "number_of_students": 1,
            "office_id": seeded_data["office_ids"]["test_office"],
            "offsite_location": "Test Office",
            "expiry_date": datetime.now().isoformat(),
            "is_pesticide": 1,
            "sbc_managed": "sbc",
            "ind_or_group": "individual",
            "fees": "25.00",
            "receipt_number": "R-100",
        },
    )
    body = json_of(response)

    assert_json_response(response, 201)
    assert body["exam"]["event_id"] == "job-Pesticide Individual"

    with app.app_context():
        from app.models.bookings import Exam

        exam = Exam.query.filter_by(exam_id=body["exam"]["exam_id"]).first()
        assert exam.exam_type_id == exam_type_id
        assert exam.office_id == seeded_data["office_ids"]["test_office"]
        assert exam.receipt == "R-100"
        assert exam.sbc_managed_ind == 1


def test_pesticide_non_sbc_exam_is_reassigned_to_the_pesticide_offsite_office(
    app, monkeypatch, internal_ga_client, seeded_data
):
    """Assert that non-SBC pesticide exams move to the dedicated pesticide office before persistence."""
    from app.resources.bookings.exam.exam_post import ExamPost

    monkeypatch.setattr(
        ExamPost.bcmp_service,
        "check_exam_status",
        lambda exam: {"jobProperties": {"JOB_ID": "job-non-sbc"}},
    )

    response = internal_ga_client.post(
        "/exams/",
        json={
            "event_id": "placeholder",
            "exam_method": "paper",
            "exam_name": "Pesticide Non SBC",
            "exam_type_id": _exam_type_id(
                app, group_exam_ind=0, ita_ind=0, pesticide_exam_ind=1
            ),
            "exam_written_ind": 0,
            "examinee_name": "Codex Examinee",
            "notes": "Pesticide non-SBC flow",
            "number_of_students": 1,
            "office_id": seeded_data["office_ids"]["test_office"],
            "offsite_location": "Test Office",
            "expiry_date": datetime.now().isoformat(),
            "is_pesticide": 1,
            "sbc_managed": "non-sbc",
            "ind_or_group": "individual",
            "fees": "25.00",
        },
    )
    body = json_of(response)

    assert_json_response(response, 201)

    with app.app_context():
        from app.models.bookings import Exam

        exam = Exam.query.filter_by(exam_id=body["exam"]["exam_id"]).first()
        assert exam.office_id == _pesticide_office_id(app)
        assert exam.event_id == "job-non-sbc"


def test_pesticide_group_exam_normalizes_candidates_and_uses_group_environment_type(
    app, monkeypatch, internal_ga_client, seeded_data
):
    """Assert that pesticide group exam creation normalizes candidate payloads for persistence."""
    from app.resources.bookings.exam.exam_post import ExamPost

    monkeypatch.setattr(
        ExamPost.bcmp_service,
        "check_exam_status",
        lambda exam: {"jobProperties": {"JOB_ID": "job-group"}},
    )
    candidate_exam_type_id = _exam_type_id(
        app, group_exam_ind=0, ita_ind=0, pesticide_exam_ind=1
    )

    response = internal_ga_client.post(
        "/exams/",
        json={
            "event_id": "placeholder",
            "exam_method": "paper",
            "exam_name": "Pesticide Group",
            "exam_type_id": _exam_type_id(
                app, exam_type_name="Group Environment Exam"
            ),
            "exam_written_ind": 0,
            "examinee_name": "Codex Group",
            "notes": "Pesticide group flow",
            "number_of_students": 2,
            "office_id": seeded_data["office_ids"]["test_office"],
            "offsite_location": "Test Office",
            "expiry_date": datetime.now().isoformat(),
            "is_pesticide": 1,
            "sbc_managed": "sbc",
            "ind_or_group": "group",
            "fees": "25.00",
            "candidates": [
                {
                    "name": "Candidate One",
                    "email": "candidate-one@example.com",
                    "exam_type_id": candidate_exam_type_id,
                    "fees": "25.00",
                    "billTo": "candidate",
                    "receipt": "R-201",
                    "payeeName": "Candidate One",
                    "payeeEmail": "candidate-one@example.com",
                },
                {
                    "name": "Candidate Two",
                    "email": "candidate-two@example.com",
                    "exam_type_id": candidate_exam_type_id,
                    "fees": "30.00",
                    "billTo": "employer",
                    "receipt": "R-202",
                    "payeeName": "Employer Two",
                    "payeeEmail": "employer-two@example.com",
                },
            ],
        },
    )
    body = json_of(response)

    assert_json_response(response, 201)

    with app.app_context():
        from app.models.bookings import Exam

        exam = Exam.query.filter_by(exam_id=body["exam"]["exam_id"]).first()
        assert exam.exam_type.exam_type_name == "Group Environment Exam"
        assert exam.event_id == "job-group"
        assert exam.candidates_list == [
            {
                "examinee_name": "Candidate One",
                "examinee_email": "candidate-one@example.com",
                "exam_type_id": candidate_exam_type_id,
                "fees": "25.00",
                "payee_ind": 1,
                "receipt": "R-201",
                "receipt_number": "R-201",
                "payee_name": "Candidate One",
                "payee_email": "candidate-one@example.com",
            },
            {
                "examinee_name": "Candidate Two",
                "examinee_email": "candidate-two@example.com",
                "exam_type_id": candidate_exam_type_id,
                "fees": "30.00",
                "payee_ind": 0,
                "receipt": "R-202",
                "receipt_number": "R-202",
                "payee_name": "Employer Two",
                "payee_email": "employer-two@example.com",
            },
        ]


def test_exam_export_all_bookings_includes_non_exam_booking_rows(
    internal_ga_client, seeded_data
):
    """Assert that the all-bookings export includes rows for bookings without attached exams."""
    booking = create_booking(
        internal_ga_client,
        seeded_data,
        days_from_now=5,
        booking_name="Booking Without Exam",
    )
    export_date = _export_date(
        booking, seeded_data["office_timezones"]["test_office"]
    )

    response = internal_ga_client.get(
        f"/exams/export/?start_date={export_date}&end_date={export_date}&exam_type=all_bookings"
    )

    assert response.status_code == 200, response.get_data(as_text=True)
    export_body = response.get_data(as_text=True)
    assert "Non Exam Booking" in export_body
    assert "Booking Without Exam" in export_body


def test_exam_export_all_non_ita_excludes_ita_exam_rows(
    app, internal_ga_client, seeded_data
):
    """Assert that the non-ITA export omits ITA exam rows while preserving non-ITA rows."""
    ita_booking = create_booking(internal_ga_client, seeded_data, days_from_now=5)
    non_ita_booking = create_booking(internal_ga_client, seeded_data, days_from_now=5)

    create_exam(
        internal_ga_client,
        seeded_data,
        ita_booking["booking_id"],
        event_id=f"ita-{uuid4().hex[:8]}",
        exam_type_id=_exam_type_id(app, group_exam_ind=0, ita_ind=1, pesticide_exam_ind=0),
        exam_name="ITA Exam",
    )
    create_exam(
        internal_ga_client,
        seeded_data,
        non_ita_booking["booking_id"],
        event_id=f"nonita-{uuid4().hex[:8]}",
        exam_type_id=_exam_type_id(
            app, group_exam_ind=0, ita_ind=0, pesticide_exam_ind=0
        ),
        exam_name="Non ITA Exam",
    )

    export_date = _export_date(
        non_ita_booking, seeded_data["office_timezones"]["test_office"]
    )
    response = internal_ga_client.get(
        f"/exams/export/?start_date={export_date}&end_date={export_date}&exam_type=all_non_ita"
    )

    assert response.status_code == 200, response.get_data(as_text=True)
    export_body = response.get_data(as_text=True)
    rows = list(csv.reader(io.StringIO(export_body)))
    exam_names = {row[3] for row in rows[1:]}
    assert "Non ITA Exam" in exam_names
    assert "ITA Exam" not in exam_names
