import pytest
from app.tests.api_test_support import assert_json_response, json_of
from app.tests.auth.auth_support import create_internal_exam_bundle, patch_exam_integrations

pytestmark = [pytest.mark.validation, pytest.mark.usefixtures("seeded_database")]


def test_exam_download_reports_when_the_package_is_not_ready(
    internal_ga_client, monkeypatch, seeded_data
):
    """Assert that exam downloads freeze the pending-package error contract."""
    _booking, exam = create_internal_exam_bundle(internal_ga_client, seeded_data)
    patch_exam_integrations(
        monkeypatch,
        download_job={"jobStatus": "QUEUED", "jobProperties": {}},
    )

    response = internal_ga_client.get(f"/exams/{exam['exam_id']}/download/")

    assert_json_response(response, 400)
    assert json_of(response) == {
        "message": "Package not yet generated",
        "status": "QUEUED",
    }


def test_exam_email_invigilator_requires_name_email_and_phone(
    internal_ga_client, monkeypatch, seeded_data
):
    """Assert that emailing an invigilator rejects incomplete contact details."""
    _booking, exam = create_internal_exam_bundle(internal_ga_client, seeded_data)
    patch_exam_integrations(monkeypatch, email_result=True)

    response = internal_ga_client.post(
        f"/exams/{exam['exam_id']}/email_invigilator/",
        json={
            "invigilator_id": seeded_data["invigilator_ids"][0],
            "invigilator_name": "Homer Simpson",
            "invigilator_email": "homer@example.com",
            "invigilator_phone": "",
        },
    )

    assert_json_response(response, 422)
    assert json_of(response)["message"] == (
        "Invigilator name, email, and phone number are required"
    )
