from __future__ import annotations

import io
from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import uuid4
from zoneinfo import ZoneInfo

import pytest
from app.tests.api_test_support import (
    assert_forbidden,
    assert_not_auth_error,
    assert_status,
    assert_unauthorized,
    create_booking,
    create_citizen,
    create_internal_appointment,
    create_queue_ready_citizen,
    create_service_ready_citizen,
    create_service_request,
    future_utc_window,
    json_of,
)
from app.tests.auth.auth_support import (
    configure_video_path,
    create_internal_exam_bundle,
    create_walkin_target,
    prepare_hold_or_finish_target,
    prepare_recurring_appointments,
    prepare_recurring_bookings,
    prepare_service_activation,
)

pytestmark = [pytest.mark.auth, pytest.mark.usefixtures("seeded_database")]


@dataclass(frozen=True)
class InternalRouteCase:
    """Describe an internal-only endpoint and how to reach its non-authenticated success path."""

    id: str
    method: str
    build_request: object
    success_assertion: object


def _assert_exact_status(expected_status: int):
    def assertion(response):
        assert_status(response, expected_status)

    return assertion


def _build_context(
    app,
    bare_client,
    internal_ga_client,
    monkeypatch,
    public_client,
    seeded_data,
    tmp_path,
):
    return {
        "app": app,
        "bare_client": bare_client,
        "internal_ga_client": internal_ga_client,
        "monkeypatch": monkeypatch,
        "public_client": public_client,
        "seeded_data": seeded_data,
        "tmp_path": tmp_path,
    }


def _build_update_csr_request(ctx):
    csr_id = ctx["seeded_data"]["csr_ids"]["ga"]
    return {"path": f"/csrs/{csr_id}/", "json": {"receptionist_ind": 1}}


def _build_update_service_request(ctx):
    citizen, service_request = create_service_ready_citizen(
        ctx["internal_ga_client"],
        ctx["seeded_data"],
        position=0,
        name="Service Request Citizen",
        service_id_key="ptax",
        channel_id_key="phone",
        quantity=1,
        counter_id_key="counter",
    )
    return {
        "path": f"/service_requests/{service_request['sr_id']}/",
        "json": {"quantity": 2},
    }


def _build_activate_service_request(ctx):
    _citizen, first_service = prepare_service_activation(
        ctx["internal_ga_client"], ctx["seeded_data"]
    )
    return {"path": f"/service_requests/{first_service['sr_id']}/activate/"}


def _build_channels_request(ctx):
    return {"path": "/channels/"}


def _build_create_service_request(ctx):
    citizen = create_citizen(
        ctx["internal_ga_client"], 0, name="Create Service Citizen"
    )
    return {
        "path": "/service_requests/",
        "json": {
            "service_request": {
                "citizen_id": citizen["citizen_id"],
                "service_id": ctx["seeded_data"]["service_ids"]["ptax"],
                "channel_id": ctx["seeded_data"]["channel_ids"]["phone"],
                "quantity": 1,
            }
        },
    }


def _build_csrs_request(ctx):
    return {"path": "/csrs/"}


def _build_csr_me_request(ctx):
    return {"path": "/csrs/me/"}


def _build_video_list_request(ctx):
    configure_video_path(
        ctx["app"],
        ctx["monkeypatch"],
        ctx["tmp_path"],
        office_number=ctx["seeded_data"]["office_numbers"]["test_office"],
    )
    return {"path": "/videofiles/"}


def _build_video_delete_request(ctx):
    configure_video_path(
        ctx["app"],
        ctx["monkeypatch"],
        ctx["tmp_path"],
        office_number=ctx["seeded_data"]["office_numbers"]["test_office"],
    )
    return {"path": "/videofiles/", "json": {"name": "sample.mp4"}}


def _build_upload_request(ctx):
    configure_video_path(
        ctx["app"],
        ctx["monkeypatch"],
        ctx["tmp_path"],
        office_number=ctx["seeded_data"]["office_numbers"]["test_office"],
    )
    return {
        "path": "/upload/",
        "data": {
            "manifest": '{"default": {"url": "https://example.com/video.mp4"}}',
            "file": (io.BytesIO(b"video-bytes"), "sample.mp4"),
        },
        "content_type": "multipart/form-data",
    }


def _build_refresh_services_request(ctx):
    return {
        "path": f"/services/refresh/?office_id={ctx['seeded_data']['office_ids']['test_office']}"
    }


def _build_remove_from_queue_request(ctx):
    citizen, _service_request = create_service_ready_citizen(
        ctx["internal_ga_client"],
        ctx["seeded_data"],
        position=0,
        name="Remove From Queue Citizen",
        service_id_key="ptax",
        channel_id_key="phone",
        quantity=1,
        counter_id_key="counter",
    )
    return {"path": f"/citizens/{citizen['citizen_id']}/remove_from_queue/"}


def _build_begin_service_request(ctx):
    citizen, _service_request = create_service_ready_citizen(
        ctx["internal_ga_client"],
        ctx["seeded_data"],
        position=0,
        name="Begin Service Citizen",
        service_id_key="ptax",
        channel_id_key="phone",
        quantity=1,
        counter_id_key="counter",
    )
    return {"path": f"/citizens/{citizen['citizen_id']}/begin_service/"}


def _build_citizen_service_requests_request(ctx):
    citizen, _service_request = create_service_ready_citizen(
        ctx["internal_ga_client"],
        ctx["seeded_data"],
        position=0,
        name="Citizen Services Lookup",
        service_id_key="ptax",
        channel_id_key="phone",
        quantity=1,
        counter_id_key="counter",
    )
    return {"path": f"/citizens/{citizen['citizen_id']}/service_requests/"}


def _build_citizen_detail_request(ctx):
    citizen = create_citizen(ctx["internal_ga_client"], 0, name="Citizen Detail")
    return {"path": f"/citizens/{citizen['citizen_id']}/"}


def _build_citizen_update_request(ctx):
    citizen = create_citizen(ctx["internal_ga_client"], 0, name="Citizen Update")
    return {
        "path": f"/citizens/{citizen['citizen_id']}/",
        "json": {"citizen_name": "Citizen Updated"},
    }


def _build_specific_invite_request(ctx):
    citizen, _service_request, _queued = create_queue_ready_citizen(
        ctx["internal_ga_client"],
        ctx["seeded_data"],
        position=0,
        name="Specific Invite Citizen",
        service_id_key="ptax",
        channel_id_key="phone",
        quantity=1,
        counter_id_key="counter",
        qt_xn_citizen_ind=0,
    )
    return {"path": f"/citizens/{citizen['citizen_id']}/invite/"}


def _build_citizen_left_request(ctx):
    citizen, _service_request = create_service_ready_citizen(
        ctx["internal_ga_client"],
        ctx["seeded_data"],
        position=0,
        name="Citizen Left",
        service_id_key="ptax",
        channel_id_key="phone",
        quantity=1,
        counter_id_key="counter",
    )
    return {"path": f"/citizens/{citizen['citizen_id']}/citizen_left/"}


def _build_add_to_queue_request(ctx):
    citizen, _service_request = create_service_ready_citizen(
        ctx["internal_ga_client"],
        ctx["seeded_data"],
        position=0,
        name="Add To Queue",
        service_id_key="ptax",
        channel_id_key="phone",
        quantity=1,
        counter_id_key="counter",
    )
    return {"path": f"/citizens/{citizen['citizen_id']}/add_to_queue/"}


def _build_finish_service_request(ctx):
    citizen = prepare_hold_or_finish_target(
        ctx["internal_ga_client"], ctx["seeded_data"]
    )
    return {"path": f"/citizens/{citizen['citizen_id']}/finish_service/"}


def _build_place_on_hold_request(ctx):
    citizen = prepare_hold_or_finish_target(
        ctx["internal_ga_client"], ctx["seeded_data"]
    )
    return {"path": f"/citizens/{citizen['citizen_id']}/place_on_hold/"}


def _build_add_citizen_request(ctx):
    return {
        "path": "/citizens/0/add_citizen/",
        "json": {"citizen_name": "Added Citizen"},
    }


def _build_generic_invite_request(ctx):
    create_queue_ready_citizen(
        ctx["internal_ga_client"],
        ctx["seeded_data"],
        position=0,
        name="Generic Invite Citizen",
        service_id_key="ptax",
        channel_id_key="phone",
        quantity=1,
        counter_id_key="counter",
        qt_xn_citizen_ind=0,
    )
    return {
        "path": "/citizens/invite/",
        "json": {"counter_id": ctx["seeded_data"]["counter_ids"]["counter"]},
    }


def _build_rooms_request(ctx):
    return {"path": "/rooms/"}


def _build_booking_detail_request(ctx):
    booking = create_booking(
        ctx["internal_ga_client"], ctx["seeded_data"], days_from_now=2
    )
    return {"path": f"/bookings/{booking['booking_id']}/"}


def _build_recurring_booking_update_request(ctx):
    recurring_uuid = prepare_recurring_bookings(
        ctx["internal_ga_client"], ctx["seeded_data"]
    )
    return {
        "path": f"/bookings/recurring/{recurring_uuid}",
        "json": {"booking_name": "Recurring Booking Updated"},
    }


def _build_recurring_booking_current_office_delete_request(ctx):
    recurring_uuid = prepare_recurring_bookings(
        ctx["internal_ga_client"], ctx["seeded_data"]
    )
    return {"path": f"/bookings/recurring/current-office/{recurring_uuid}"}


def _build_recurring_booking_stat_delete_request(ctx):
    recurring_uuid = prepare_recurring_bookings(
        ctx["internal_ga_client"], ctx["seeded_data"]
    )
    return {"path": f"/bookings/recurring/stat/{recurring_uuid}"}


def _build_booking_create_request(ctx):
    start_time, end_time = future_utc_window(2, duration_minutes=120)
    return {
        "path": "/bookings/",
        "json": {
            "booking_name": f"Auth Booking {uuid4().hex[:6]}",
            "booking_contact_information": "booking@example.com",
            "fees": "false",
            "office_id": ctx["seeded_data"]["office_ids"]["test_office"],
            "room_id": ctx["seeded_data"]["room_id"],
            "start_time": start_time,
            "end_time": end_time,
            "invigilator_id": [ctx["seeded_data"]["invigilator_ids"][0]],
        },
    }


def _build_invigilator_update_request(ctx):
    invigilator_id = ctx["seeded_data"]["invigilator_ids"][0]
    return {"path": f"/invigilator/{invigilator_id}/?subtract=True&add=False"}


def _build_invigilator_list_request(ctx):
    return {"path": "/invigilators/"}


def _build_booking_delete_request(ctx):
    booking = create_booking(
        ctx["internal_ga_client"], ctx["seeded_data"], days_from_now=2
    )
    return {"path": f"/bookings/{booking['booking_id']}/"}


def _build_booking_list_request(ctx):
    return {"path": "/bookings/"}


def _build_booking_recurring_delete_request(ctx):
    recurring_uuid = prepare_recurring_bookings(
        ctx["internal_ga_client"], ctx["seeded_data"]
    )
    return {"path": f"/bookings/recurring/{recurring_uuid}"}


def _build_walkin_reminder_request(ctx):
    citizen, _walkin_id = create_walkin_target(
        ctx["app"], ctx["internal_ga_client"], ctx["seeded_data"]
    )
    return {
        "path": "/send-reminder/line-walkin/",
        "json": {"previous_citizen_id": citizen["citizen_id"]},
    }


def _build_appointment_recurring_update_request(ctx):
    recurring_uuid = prepare_recurring_appointments(
        ctx["internal_ga_client"], ctx["seeded_data"]
    )
    return {
        "path": f"/appointments/recurring/{recurring_uuid}",
        "json": {"comments": "Recurring appointment updated"},
    }


def _build_appointment_all_stat_delete_request(ctx):
    recurring_uuid = prepare_recurring_appointments(
        ctx["internal_ga_client"], ctx["seeded_data"]
    )
    return {"path": f"/appointments/all-stat/{recurring_uuid}"}


def _build_appointment_list_request(ctx):
    return {"path": "/appointments/"}


def _build_appointment_recurring_delete_request(ctx):
    recurring_uuid = prepare_recurring_appointments(
        ctx["internal_ga_client"], ctx["seeded_data"]
    )
    return {"path": f"/appointments/recurring/{recurring_uuid}"}


def _build_appointment_detail_request(ctx):
    appointment = create_internal_appointment(
        ctx["internal_ga_client"], ctx["seeded_data"], days_from_now=2
    )
    return {"path": f"/appointments/{appointment['appointment_id']}/"}


def _build_exam_create_request(ctx):
    booking = create_booking(
        ctx["internal_ga_client"], ctx["seeded_data"], days_from_now=5
    )
    return {
        "path": "/exams/",
        "json": {
            "booking_id": booking["booking_id"],
            "event_id": f"auth-event-{uuid4().hex[:6]}",
            "exam_method": "paper",
            "exam_name": "Auth Exam",
            "exam_type_id": ctx["seeded_data"]["exam_type_id"],
            "exam_written_ind": 0,
            "examinee_name": "Auth Examinee",
            "notes": "Auth exam notes",
            "number_of_students": 19,
            "office_id": ctx["seeded_data"]["office_ids"]["test_office"],
            "offsite_location": "Test Office",
            "expiry_date": datetime.now(timezone.utc)
            .replace(microsecond=0)
            .isoformat(),
        },
    }


def _build_exam_type_list_request(ctx):
    return {"path": "/exam_types/"}


def _build_exam_update_request(ctx):
    _booking, exam = create_internal_exam_bundle(
        ctx["internal_ga_client"], ctx["seeded_data"]
    )
    return {
        "path": f"/exams/{exam['exam_id']}/",
        "json": {"exam_name": "Updated Auth Exam"},
    }


def _build_exam_detail_request(ctx):
    _booking, exam = create_internal_exam_bundle(
        ctx["internal_ga_client"], ctx["seeded_data"]
    )
    return {"path": f"/exams/{exam['exam_id']}/"}


def _build_exam_list_request(ctx):
    return {"path": "/exams/"}


def _build_exam_export_request(ctx):
    booking, _exam = create_internal_exam_bundle(
        ctx["internal_ga_client"], ctx["seeded_data"]
    )
    export_date = (
        datetime.fromisoformat(booking["start_time"].replace("Z", "+00:00"))
        .astimezone(ZoneInfo(ctx["seeded_data"]["office_timezones"]["test_office"]))
        .date()
    )
    return {
        "path": f"/exams/export/?start_date={export_date.isoformat()}&end_date={export_date.isoformat()}"
    }


def _build_exam_delete_request(ctx):
    _booking, exam = create_internal_exam_bundle(
        ctx["internal_ga_client"], ctx["seeded_data"]
    )
    return {"path": f"/exams/{exam['exam_id']}/"}


def _build_exam_event_lookup_request(ctx):
    booking = create_booking(
        ctx["internal_ga_client"], ctx["seeded_data"], days_from_now=5
    )
    event_id = 9000 + booking["booking_id"]
    create_exam_response = ctx["internal_ga_client"].post(
        "/exams/",
        json={
            "booking_id": booking["booking_id"],
            "event_id": str(event_id),
            "exam_method": "paper",
            "exam_name": "Lookup Exam",
            "exam_type_id": ctx["seeded_data"]["exam_type_id"],
            "exam_written_ind": 0,
            "examinee_name": "Lookup Examinee",
            "notes": "Lookup exam notes",
            "number_of_students": 19,
            "office_id": ctx["seeded_data"]["office_ids"]["test_office"],
            "offsite_location": "Test Office",
            "expiry_date": datetime.now(timezone.utc)
            .replace(microsecond=0)
            .isoformat(),
        },
    )
    assert_status(create_exam_response, 201)
    return {"path": f"/exams/event_id/{event_id}/"}


INTERNAL_ONLY_CASES = [
    InternalRouteCase(
        "PUT /csrs/<id>/", "PUT", _build_update_csr_request, _assert_exact_status(200)
    ),
    InternalRouteCase(
        "PUT /service_requests/<id>/",
        "PUT",
        _build_update_service_request,
        _assert_exact_status(200),
    ),
    InternalRouteCase(
        "POST /service_requests/<id>/activate/",
        "POST",
        _build_activate_service_request,
        _assert_exact_status(200),
    ),
    InternalRouteCase(
        "GET /channels/", "GET", _build_channels_request, _assert_exact_status(200)
    ),
    InternalRouteCase(
        "POST /service_requests/",
        "POST",
        _build_create_service_request,
        _assert_exact_status(201),
    ),
    InternalRouteCase(
        "GET /csrs/", "GET", _build_csrs_request, _assert_exact_status(200)
    ),
    InternalRouteCase(
        "GET /csrs/me/", "GET", _build_csr_me_request, _assert_exact_status(200)
    ),
    InternalRouteCase(
        "GET /videofiles/", "GET", _build_video_list_request, _assert_exact_status(200)
    ),
    InternalRouteCase(
        "DELETE /videofiles/",
        "DELETE",
        _build_video_delete_request,
        _assert_exact_status(204),
    ),
    InternalRouteCase(
        "POST /upload/", "POST", _build_upload_request, assert_not_auth_error
    ),
    InternalRouteCase(
        "GET /services/refresh/",
        "GET",
        _build_refresh_services_request,
        _assert_exact_status(200),
    ),
    InternalRouteCase(
        "POST /citizens/<id>/remove_from_queue/",
        "POST",
        _build_remove_from_queue_request,
        assert_not_auth_error,
    ),
    InternalRouteCase(
        "POST /citizens/<id>/begin_service/",
        "POST",
        _build_begin_service_request,
        _assert_exact_status(200),
    ),
    InternalRouteCase(
        "GET /citizens/<id>/service_requests/",
        "GET",
        _build_citizen_service_requests_request,
        _assert_exact_status(200),
    ),
    InternalRouteCase(
        "GET /citizens/<id>/",
        "GET",
        _build_citizen_detail_request,
        _assert_exact_status(200),
    ),
    InternalRouteCase(
        "PUT /citizens/<id>/",
        "PUT",
        _build_citizen_update_request,
        _assert_exact_status(200),
    ),
    InternalRouteCase(
        "POST /citizens/<id>/invite/",
        "POST",
        _build_specific_invite_request,
        _assert_exact_status(200),
    ),
    InternalRouteCase(
        "POST /citizens/<id>/citizen_left/",
        "POST",
        _build_citizen_left_request,
        _assert_exact_status(200),
    ),
    InternalRouteCase(
        "POST /citizens/<id>/add_to_queue/",
        "POST",
        _build_add_to_queue_request,
        _assert_exact_status(200),
    ),
    InternalRouteCase(
        "POST /citizens/<id>/finish_service/",
        "POST",
        _build_finish_service_request,
        _assert_exact_status(200),
    ),
    InternalRouteCase(
        "POST /citizens/<id>/place_on_hold/",
        "POST",
        _build_place_on_hold_request,
        _assert_exact_status(200),
    ),
    InternalRouteCase(
        "POST /citizens/<citizens_waiting>/add_citizen/",
        "POST",
        _build_add_citizen_request,
        _assert_exact_status(201),
    ),
    InternalRouteCase(
        "POST /citizens/invite/",
        "POST",
        _build_generic_invite_request,
        _assert_exact_status(200),
    ),
    InternalRouteCase(
        "GET /rooms/", "GET", _build_rooms_request, _assert_exact_status(200)
    ),
    InternalRouteCase(
        "GET /bookings/<id>/",
        "GET",
        _build_booking_detail_request,
        _assert_exact_status(200),
    ),
    InternalRouteCase(
        "PUT /bookings/recurring/<id>",
        "PUT",
        _build_recurring_booking_update_request,
        _assert_exact_status(200),
    ),
    InternalRouteCase(
        "DELETE /bookings/recurring/current-office/<id>",
        "DELETE",
        _build_recurring_booking_current_office_delete_request,
        _assert_exact_status(204),
    ),
    InternalRouteCase(
        "DELETE /bookings/recurring/stat/<id>",
        "DELETE",
        _build_recurring_booking_stat_delete_request,
        _assert_exact_status(204),
    ),
    InternalRouteCase(
        "POST /bookings/",
        "POST",
        _build_booking_create_request,
        _assert_exact_status(201),
    ),
    InternalRouteCase(
        "PUT /invigilator/<id>/",
        "PUT",
        _build_invigilator_update_request,
        _assert_exact_status(200),
    ),
    InternalRouteCase(
        "GET /invigilators/",
        "GET",
        _build_invigilator_list_request,
        _assert_exact_status(200),
    ),
    InternalRouteCase(
        "DELETE /bookings/<id>/",
        "DELETE",
        _build_booking_delete_request,
        _assert_exact_status(204),
    ),
    InternalRouteCase(
        "GET /bookings/", "GET", _build_booking_list_request, _assert_exact_status(200)
    ),
    InternalRouteCase(
        "DELETE /bookings/recurring/<id>",
        "DELETE",
        _build_booking_recurring_delete_request,
        _assert_exact_status(204),
    ),
    InternalRouteCase(
        "POST /send-reminder/line-walkin/",
        "POST",
        _build_walkin_reminder_request,
        _assert_exact_status(200),
    ),
    InternalRouteCase(
        "PUT /appointments/recurring/<id>",
        "PUT",
        _build_appointment_recurring_update_request,
        _assert_exact_status(200),
    ),
    InternalRouteCase(
        "DELETE /appointments/all-stat/<id>",
        "DELETE",
        _build_appointment_all_stat_delete_request,
        _assert_exact_status(204),
    ),
    InternalRouteCase(
        "GET /appointments/",
        "GET",
        _build_appointment_list_request,
        _assert_exact_status(200),
    ),
    InternalRouteCase(
        "DELETE /appointments/recurring/<id>",
        "DELETE",
        _build_appointment_recurring_delete_request,
        _assert_exact_status(204),
    ),
    InternalRouteCase(
        "GET /appointments/<id>/",
        "GET",
        _build_appointment_detail_request,
        _assert_exact_status(200),
    ),
    InternalRouteCase(
        "POST /exams/", "POST", _build_exam_create_request, _assert_exact_status(201)
    ),
    InternalRouteCase(
        "GET /exam_types/",
        "GET",
        _build_exam_type_list_request,
        _assert_exact_status(200),
    ),
    InternalRouteCase(
        "PUT /exams/<id>/", "PUT", _build_exam_update_request, _assert_exact_status(201)
    ),
    InternalRouteCase(
        "GET /exams/<id>/", "GET", _build_exam_detail_request, _assert_exact_status(200)
    ),
    InternalRouteCase(
        "GET /exams/", "GET", _build_exam_list_request, _assert_exact_status(200)
    ),
    InternalRouteCase(
        "GET /exams/export/",
        "GET",
        _build_exam_export_request,
        _assert_exact_status(200),
    ),
    InternalRouteCase(
        "DELETE /exams/<id>/",
        "DELETE",
        _build_exam_delete_request,
        _assert_exact_status(204),
    ),
    InternalRouteCase(
        "GET /exams/event_id/<id>/",
        "GET",
        _build_exam_event_lookup_request,
        _assert_exact_status(200),
    ),
]


@pytest.mark.parametrize("case", INTERNAL_ONLY_CASES, ids=lambda case: case.id)
def test_bare_client_receives_401_for_internal_only_routes(
    app,
    bare_client,
    case,
    internal_ga_client,
    monkeypatch,
    public_client,
    seeded_data,
    tmp_path,
):
    """Assert that internal-only routes reject unauthenticated requests."""
    ctx = _build_context(
        app,
        bare_client,
        internal_ga_client,
        monkeypatch,
        public_client,
        seeded_data,
        tmp_path,
    )
    request_kwargs = case.build_request(ctx)

    response = bare_client.open(
        request_kwargs.pop("path"), method=case.method, **request_kwargs
    )

    assert_unauthorized(response)


@pytest.mark.parametrize("case", INTERNAL_ONLY_CASES, ids=lambda case: case.id)
def test_public_user_receives_403_for_internal_only_routes(
    app,
    bare_client,
    case,
    internal_ga_client,
    monkeypatch,
    public_client,
    seeded_data,
    tmp_path,
):
    """Assert that public users remain forbidden from internal-only routes."""
    ctx = _build_context(
        app,
        bare_client,
        internal_ga_client,
        monkeypatch,
        public_client,
        seeded_data,
        tmp_path,
    )
    request_kwargs = case.build_request(ctx)

    response = public_client.open(
        request_kwargs.pop("path"), method=case.method, **request_kwargs
    )

    assert_forbidden(response)


@pytest.mark.parametrize("case", INTERNAL_ONLY_CASES, ids=lambda case: case.id)
def test_internal_user_reaches_non_auth_behavior_for_internal_only_routes(
    app,
    bare_client,
    case,
    internal_ga_client,
    monkeypatch,
    public_client,
    seeded_data,
    tmp_path,
):
    """Assert that internal users still reach each internal-only route's non-auth behavior."""
    ctx = _build_context(
        app,
        bare_client,
        internal_ga_client,
        monkeypatch,
        public_client,
        seeded_data,
        tmp_path,
    )
    request_kwargs = case.build_request(ctx)

    response = internal_ga_client.open(
        request_kwargs.pop("path"), method=case.method, **request_kwargs
    )

    case.success_assertion(response)
