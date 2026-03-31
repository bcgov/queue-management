import pytest
from app.tests.api_test_support import (
    assert_forbidden,
    assert_json_response,
    assert_unauthorized,
    json_of,
)

pytestmark = [pytest.mark.auth, pytest.mark.usefixtures("seeded_database")]


def test_bare_client_receives_401_for_reminder_job_routes(bare_client):
    """Assert that reminder-job routes still reject unauthenticated callers."""
    response = bare_client.get("/appointment/reminders/email/")

    assert_unauthorized(response)


def test_internal_user_receives_403_for_reminder_job_routes(internal_ga_client):
    """Assert that regular internal identities remain forbidden from reminder-job routes."""
    response = internal_ga_client.get("/appointment/reminders/email/")

    assert_forbidden(response)


def test_public_user_receives_403_for_reminder_job_routes(public_client):
    """Assert that public identities remain forbidden from reminder-job routes."""
    response = public_client.get("/appointment/reminders/email/")

    assert_forbidden(response)


def test_reminder_job_identity_can_access_reminder_routes(reminder_job_client):
    """Assert that the synthetic reminder-job identity can still reach reminder routes."""
    response = reminder_job_client.get("/appointment/reminders/email/")

    assert_json_response(response, 200)
    assert "appointments" in json_of(response)
