import pytest
from app.tests.api_test_support import assert_json_response, json_of
from app.tests.auth.auth_support import (
    build_bcmp_exam_payload,
    create_internal_exam_bundle,
    patch_exam_integrations,
)
from app.tests.helpers.exams import (
    exam_invigilator_id,
    exam_upload_received_ind,
    seed_exam_bcmp_job,
)

pytestmark = [pytest.mark.flows, pytest.mark.usefixtures("seeded_database")]


def test_bcmp_exam_create_returns_the_bcmp_job_id(
    internal_ga_client, monkeypatch, seeded_data
):
    """Assert that BCMP exam creation returns the created job id."""
    patch_exam_integrations(
        monkeypatch, create_individual_response={"jobId": "bcmp-job-999"}
    )

    response = internal_ga_client.post(
        "/exams/bcmp/",
        json=build_bcmp_exam_payload(seeded_data),
    )

    assert_json_response(response, 201)
    assert json_of(response)["bcmp_job_id"] == "bcmp-job-999"


def test_bcmp_status_marks_uploaded_exams_as_received(
    app, internal_ga_client, monkeypatch, seeded_data
):
    """Assert that BCMP bulk status updates persist upload_received_ind for matching exams."""
    _booking, exam = create_internal_exam_bundle(internal_ga_client, seeded_data)
    seed_exam_bcmp_job(
        app,
        exam["exam_id"],
        bcmp_job_id="bcmp-job-555",
        upload_received_ind=0,
    )
    patch_exam_integrations(
        monkeypatch,
        bulk_jobs=[{"jobId": "bcmp-job-555", "jobStatus": "RESPONSE_UPLOADED"}],
    )

    response = internal_ga_client.post("/exams/bcmp_status/", json={})

    assert_json_response(response, 200)
    assert json_of(response)["exams_updated"] == [exam["exam_id"]]
    assert exam_upload_received_ind(app, exam["exam_id"]) == 1


def test_exam_transfer_returns_the_bcmp_transfer_response(
    internal_ga_client, monkeypatch, seeded_data
):
    """Assert that exam transfer returns the accepted BCMP response payload."""
    _booking, exam = create_internal_exam_bundle(internal_ga_client, seeded_data)
    patch_exam_integrations(
        monkeypatch, transfer_response={"jobId": "transfer-job-999"}
    )

    response = internal_ga_client.post(f"/exams/{exam['exam_id']}/transfer/")

    assert_json_response(response, 202)
    assert json_of(response)["bcmp"]["jobId"] == "transfer-job-999"


def test_exam_download_returns_the_generated_pdf(
    internal_ga_client, monkeypatch, seeded_data
):
    """Assert that exam downloads stream the generated PDF bytes when the package is ready."""
    _booking, exam = create_internal_exam_bundle(internal_ga_client, seeded_data)
    patch_exam_integrations(
        monkeypatch,
        download_job={
            "jobStatus": "PACKAGE_GENERATED",
            "jobProperties": {"EXAM_PACKAGE_URL": "https://example.com/package.pdf"},
        },
        download_bytes=b"exam-pdf",
    )

    response = internal_ga_client.get(f"/exams/{exam['exam_id']}/download/")

    assert response.status_code == 200, response.get_data(as_text=True)
    assert response.mimetype == "application/pdf"
    assert response.get_data() == b"exam-pdf"


def test_email_invigilator_updates_the_exam_record(
    app, internal_ga_client, monkeypatch, seeded_data
):
    """Assert that emailing the invigilator persists the selected invigilator on the exam."""
    _booking, exam = create_internal_exam_bundle(internal_ga_client, seeded_data)
    patch_exam_integrations(monkeypatch, email_result=True)

    response = internal_ga_client.post(
        f"/exams/{exam['exam_id']}/email_invigilator/",
        json={
            "invigilator_id": seeded_data["invigilator_ids"][0],
            "invigilator_name": "Homer Simpson",
            "invigilator_email": "homer@example.com",
            "invigilator_phone": "2505550100",
        },
    )

    assert_json_response(response, 200)
    assert exam_invigilator_id(app, exam["exam_id"]) == seeded_data["invigilator_ids"][0]
