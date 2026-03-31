from __future__ import annotations

import io
import json
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from app.tests.api_test_support import (
    assert_json_response,
    create_booking,
    create_exam,
    create_internal_appointment,
    create_public_user,
    create_queue_ready_citizen,
    create_service_ready_citizen,
    create_service_request,
    json_of,
    public_slot_payload,
)


def configure_video_path(
    app, monkeypatch, tmp_path: Path, *, office_number: int
) -> Path:
    """Create a disposable video directory and point the app config at it."""
    video_dir = tmp_path / "videos"
    video_dir.mkdir()
    (video_dir / "sample.mp4").write_bytes(b"video-bytes")
    (video_dir / "manifest.json").write_text(
        json.dumps(
            {
                str(office_number): {"url": "https://example.com/office-video.mp4"},
                "default": {"url": "https://example.com/default-video.mp4"},
            }
        )
    )
    monkeypatch.setitem(app.config, "VIDEO_PATH", str(video_dir))
    return video_dir


def create_public_appointment(public_client, seeded_data) -> dict:
    """Create an appointment owned by the authenticated public test user."""
    create_public_user(public_client)
    payload, _day_key, _slots = public_slot_payload(
        public_client, seeded_data, minimum_slots=1
    )
    response = public_client.post("/appointments/", json=payload)
    assert_json_response(response, 201)
    return json_of(response)["appointment"]


def create_internal_exam_bundle(internal_ga_client, seeded_data) -> tuple[dict, dict]:
    """Create a booking plus exam pair for exam-auth tests."""
    booking = create_booking(internal_ga_client, seeded_data, days_from_now=5)
    exam = create_exam(
        internal_ga_client,
        seeded_data,
        booking["booking_id"],
        event_id=f"event-{uuid4().hex[:8]}",
    )
    return booking, exam


def create_walkin_target(app, internal_ga_client, seeded_data) -> tuple[dict, str]:
    """Create a queued citizen and persist a walk-in identifier for open walk-in routes."""
    citizen, _service_request, _queued = create_queue_ready_citizen(
        internal_ga_client,
        seeded_data,
        position=0,
        name="Walkin Citizen",
        service_id_key="ptax",
        channel_id_key="phone",
        quantity=1,
        counter_id_key="counter",
        qt_xn_citizen_ind=0,
        comments="Walkin citizen",
    )
    walkin_id = f"walkin-{uuid4().hex[:8]}"

    with app.app_context():
        from app.models.theq import Citizen
        from qsystem import db

        citizen_model = Citizen.find_citizen_by_id(citizen["citizen_id"])
        citizen_model.walkin_unique_id = walkin_id
        citizen_model.notification_phone = "2505550100"
        citizen_model.start_position = 1
        db.session.add(citizen_model)
        db.session.commit()

    return citizen, walkin_id


def promote_internal_csr_to_support(app, *, username="cfms-postman-non-operator"):
    """Promote a seeded internal CSR to SUPPORT for role-specific integration tests."""
    with app.app_context():
        from app.models.theq import CSR, Role
        from qsystem import db

        csr = CSR.query.filter_by(username=username).first()
        support_role = Role.query.filter_by(role_code="SUPPORT").first()
        csr.role_id = support_role.role_id
        db.session.add(csr)
        db.session.commit()
        return csr.csr_id


def patch_exam_integrations(
    monkeypatch,
    *,
    create_individual_response=None,
    create_group_response=None,
    bulk_jobs=None,
    transfer_response=None,
    email_result=True,
    download_job=None,
    download_bytes=b"pdf-bytes",
):
    """Replace BCMP and MinIO calls with deterministic local stubs."""
    from app.resources.bookings.exam.exam_bcmp import ExamBcmpPost
    from app.resources.bookings.exam.exam_bulk_status import ExamList
    from app.resources.bookings.exam.exam_download import (
        ExamStatus as ExamDownloadStatus,
    )
    from app.resources.bookings.exam.exam_email_invigilator import ExamEmailInvigilator
    from app.resources.bookings.exam.exam_transfer import (
        ExamStatus as ExamTransferStatus,
    )
    from app.utilities.document_service import DocumentService

    if create_individual_response is None:
        create_individual_response = {"jobId": "bcmp-job-123"}
    if create_group_response is None:
        create_group_response = {"jobId": "bcmp-group-job-123"}
    if bulk_jobs is None:
        bulk_jobs = []
    if transfer_response is None:
        transfer_response = {"jobId": "transfer-job-123"}
    if download_job is None:
        download_job = {
            "jobStatus": "PACKAGE_GENERATED",
            "jobProperties": {"EXAM_PACKAGE_URL": "https://example.com/package.pdf"},
        }

    monkeypatch.setattr(
        ExamBcmpPost.bcmp_service,
        "create_individual_exam",
        lambda *args, **kwargs: create_individual_response,
    )
    monkeypatch.setattr(
        ExamBcmpPost.bcmp_service,
        "create_group_exam_bcmp",
        lambda *args, **kwargs: create_group_response,
    )
    monkeypatch.setattr(
        ExamList.bcmp_service,
        "bulk_check_exam_status",
        lambda exams: {"jobs": list(bulk_jobs)},
    )
    monkeypatch.setattr(
        ExamTransferStatus.bcmp_service,
        "send_exam_to_bcmp",
        lambda exam: transfer_response,
    )
    monkeypatch.setattr(
        ExamEmailInvigilator.bcmp_service,
        "email_exam_invigilator",
        lambda *args, **kwargs: email_result,
    )
    monkeypatch.setattr(
        ExamDownloadStatus.bcmp_service,
        "check_exam_status",
        lambda exam: download_job,
    )
    monkeypatch.setattr(
        DocumentService,
        "get_presigned_put_url",
        lambda self, name: "https://example.com/upload",
    )

    from app.resources.bookings.exam import exam_download as exam_download_module

    monkeypatch.setattr(
        exam_download_module.urllib.request,
        "urlopen",
        lambda request: io.BytesIO(download_bytes),
    )


def build_bcmp_exam_payload(seeded_data) -> dict:
    """Build a minimal BCMP exam payload that reaches the authenticated code path."""
    return {
        "event_id": f"bcmp-{uuid4().hex[:8]}",
        "exam_method": "paper",
        "exam_name": "Environment",
        "exam_type_id": seeded_data["exam_type_id"],
        "exam_written_ind": 0,
        "examinee_name": "BCMP Examinee",
        "notes": "BCMP auth test",
        "number_of_students": 1,
        "office_id": seeded_data["office_ids"]["test_office"],
        "offsite_location": "Test Office",
        "expiry_date": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "is_pesticide": 1,
        "sbc_managed": "sbc",
        "ind_or_group": "individual",
        "fees": "25.00",
    }


def prepare_service_activation(api_client, seeded_data) -> tuple[dict, dict]:
    """Create two service requests so the first one can be reactivated."""
    citizen, first_service = create_service_ready_citizen(
        api_client,
        seeded_data,
        position=0,
        name="Activation Citizen",
        service_id_key="ptax",
        channel_id_key="phone",
        quantity=1,
        counter_id_key="counter",
    )
    create_service_request(
        api_client,
        citizen["citizen_id"],
        service_id=seeded_data["service_ids"]["msp"],
        channel_id=seeded_data["channel_ids"]["email"],
        quantity=1,
    )
    return citizen, first_service


def prepare_hold_or_finish_target(api_client, seeded_data) -> dict:
    """Create a citizen and advance them to the Being Served state."""
    citizen, _service_request = create_service_ready_citizen(
        api_client,
        seeded_data,
        position=0,
        name="Serving Citizen",
        service_id_key="ptax",
        channel_id_key="phone",
        quantity=1,
        counter_id_key="counter",
    )
    api_client.post(f"/citizens/{citizen['citizen_id']}/begin_service/")
    return citizen


def prepare_recurring_bookings(api_client, seeded_data) -> str:
    """Create recurring bookings and return the shared recurring UUID."""
    recurring_uuid = str(uuid4())
    create_booking(
        api_client, seeded_data, days_from_now=3, recurring_uuid=recurring_uuid
    )
    create_booking(
        api_client, seeded_data, days_from_now=4, recurring_uuid=recurring_uuid
    )
    return recurring_uuid


def prepare_recurring_appointments(api_client, seeded_data) -> str:
    """Create recurring appointments and return the shared recurring UUID."""
    recurring_uuid = str(uuid4())
    create_internal_appointment(
        api_client, seeded_data, days_from_now=3, recurring_uuid=recurring_uuid
    )
    create_internal_appointment(
        api_client, seeded_data, days_from_now=4, recurring_uuid=recurring_uuid
    )
    return recurring_uuid
