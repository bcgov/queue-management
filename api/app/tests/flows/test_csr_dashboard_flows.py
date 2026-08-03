from __future__ import annotations

from datetime import timedelta
from uuid import uuid4

import pytest
from app.tests.api_test_support import (
    assert_json_response,
    create_booking,
    create_exam,
    create_service_ready_citizen,
    json_of,
)

pytestmark = [pytest.mark.flows, pytest.mark.usefixtures("seeded_database")]


def _exam_type_id(
    app,
    *,
    group_exam_ind: int | None = None,
    ita_ind: int | None = None,
    pesticide_exam_ind: int | None = None,
):
    with app.app_context():
        from app.models.bookings import ExamType

        query = ExamType.query
        if group_exam_ind is not None:
            query = query.filter_by(group_exam_ind=group_exam_ind)
        if ita_ind is not None:
            query = query.filter_by(ita_ind=ita_ind)
        if pesticide_exam_ind is not None:
            query = query.filter_by(pesticide_exam_ind=pesticide_exam_ind)

        exam_type = query.order_by(ExamType.exam_type_id).first()
        assert exam_type is not None
        return exam_type.exam_type_id


def test_csr_me_reports_active_citizens_for_the_logged_in_csr(
    internal_ga_client, seeded_data
):
    """Assert that csr-self lists in-progress citizens already being served by the caller."""
    citizen, _service_request = create_service_ready_citizen(
        internal_ga_client,
        seeded_data,
        position=0,
        name="Dashboard Citizen",
        service_id_key="ptax",
        channel_id_key="phone",
        quantity=1,
        counter_id_key="counter",
    )
    begin_service = internal_ga_client.post(
        f"/citizens/{citizen['citizen_id']}/begin_service/"
    )
    assert_json_response(begin_service, 200)

    response = internal_ga_client.get("/csrs/me/")
    body = json_of(response)

    assert_json_response(response, 200)
    assert body["attention_needed"] is False
    assert citizen["citizen_id"] in {
        active_citizen["citizen_id"] for active_citizen in body["active_citizens"]
    }


def test_csr_me_flags_attention_for_stale_individual_exams(
    app, internal_ga_client, seeded_data
):
    """Assert that overdue individual exams surface the exam-manager attention banner."""
    booking = create_booking(internal_ga_client, seeded_data, days_from_now=5)
    create_exam(
        internal_ga_client,
        seeded_data,
        booking["booking_id"],
        event_id=f"stale-{uuid4().hex[:8]}",
        exam_type_id=_exam_type_id(app, group_exam_ind=0, ita_ind=1),
    )

    with app.app_context():
        from app.models.bookings import Booking
        from qsystem import db

        booking_model = Booking.query.filter_by(booking_id=booking["booking_id"]).first()
        duration = booking_model.end_time - booking_model.start_time
        booking_model.start_time = booking_model.start_time - timedelta(days=10)
        booking_model.end_time = booking_model.start_time + duration
        db.session.add(booking_model)
        db.session.commit()

    response = internal_ga_client.get("/csrs/me/")

    assert_json_response(response, 200)
    assert json_of(response)["attention_needed"] is True


def test_csr_me_flags_attention_for_missing_pesticide_receipts(
    app, internal_ga_client, seeded_data
):
    """Assert that pesticide exams without a received date keep the dashboard alert active."""
    booking = create_booking(internal_ga_client, seeded_data, days_from_now=5)
    exam = create_exam(
        internal_ga_client,
        seeded_data,
        booking["booking_id"],
        event_id=f"pest-{uuid4().hex[:8]}",
        exam_type_id=_exam_type_id(
            app, group_exam_ind=0, ita_ind=0, pesticide_exam_ind=1
        ),
    )

    with app.app_context():
        from app.models.bookings import Exam
        from qsystem import db

        exam_model = Exam.query.filter_by(exam_id=exam["exam_id"]).first()
        exam_model.is_pesticide = 1
        exam_model.exam_received_date = None
        db.session.add(exam_model)
        db.session.commit()

    response = internal_ga_client.get("/csrs/me/")

    assert_json_response(response, 200)
    assert json_of(response)["attention_needed"] is True


@pytest.mark.parametrize(
    ("student_count", "invigilator_count"),
    [
        pytest.param(10, 0, id="small-group-requires-at-least-one-invigilator"),
        pytest.param(25, 1, id="large-group-requires-two-invigilators"),
    ],
)
def test_csr_me_flags_attention_for_group_exam_invigilator_thresholds(
    app, internal_ga_client, seeded_data, student_count, invigilator_count
):
    """Assert that the csr dashboard flags understaffed group-exam bookings."""
    booking = create_booking(
        internal_ga_client,
        seeded_data,
        days_from_now=5,
        invigilator_ids=seeded_data["invigilator_ids"][:invigilator_count],
    )
    create_exam(
        internal_ga_client,
        seeded_data,
        booking["booking_id"],
        event_id=f"group-{student_count}-{uuid4().hex[:8]}",
        exam_type_id=_exam_type_id(app, group_exam_ind=1, ita_ind=1),
        number_of_students=student_count,
    )

    response = internal_ga_client.get("/csrs/me/")

    assert_json_response(response, 200)
    assert json_of(response)["attention_needed"] is True
