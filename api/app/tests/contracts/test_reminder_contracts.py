import pytest
from app.tests.api_test_support import assert_json_response, json_of
from app.tests.auth.auth_support import create_public_appointment
from app.tests.contracts.conftest import validate_schema
from app.tests.contracts.schemas import REMINDER_RESPONSE_SCHEMA
from app.tests.helpers.appointments import (
    align_current_pacific_time_for_appointment,
    configure_public_user_reminders,
    create_internal_reminder_appointment,
)

pytestmark = [pytest.mark.contracts, pytest.mark.usefixtures("seeded_database")]


def test_email_reminder_response_matches_the_contract(
    internal_ga_client, monkeypatch, reminder_job_client, seeded_data
):
    """Assert that email reminders return the stable payload contract for anonymous appointments."""
    appointment = create_internal_reminder_appointment(
        internal_ga_client,
        seeded_data,
        contact_information="anonymous@example.com",
    )
    align_current_pacific_time_for_appointment(
        monkeypatch,
        appointment["start_time"],
        seeded_data["office_timezones"]["test_office"],
    )

    response = reminder_job_client.get("/appointment/reminders/email/")
    body = json_of(response)

    assert_json_response(response, 200)
    validate_schema(body, REMINDER_RESPONSE_SCHEMA)
    assert any(item["email"] == "anonymous@example.com" for item in body["appointments"])


def test_sms_reminder_response_matches_the_contract(
    monkeypatch, public_client, reminder_job_client, seeded_data
):
    """Assert that SMS reminders return the stable payload contract for opted-in public users."""
    user = configure_public_user_reminders(
        public_client,
        email="public@example.com",
        telephone="2505550100",
        send_sms_reminders=True,
    )
    appointment = create_public_appointment(public_client, seeded_data)
    align_current_pacific_time_for_appointment(
        monkeypatch,
        appointment["start_time"],
        seeded_data["office_timezones"]["limited_office"],
    )

    response = reminder_job_client.get("/appointment/reminders/sms/")
    body = json_of(response)

    assert_json_response(response, 200)
    validate_schema(body, REMINDER_RESPONSE_SCHEMA)
    assert any(
        item["display_name"] == user["display_name"]
        and item["user_telephone"] == "2505550100"
        for item in body["appointments"]
    )
