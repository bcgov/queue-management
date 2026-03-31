import pytest
from app.tests.api_test_support import assert_json_response, json_of
from app.tests.auth.auth_support import create_public_appointment
from app.tests.helpers.appointments import (
    align_current_pacific_time_for_appointment,
    configure_public_user_reminders,
    create_internal_reminder_appointment,
)

pytestmark = [pytest.mark.flows, pytest.mark.usefixtures("seeded_database")]


def test_email_reminders_include_opted_in_public_users(
    monkeypatch, public_client, reminder_job_client, seeded_data
):
    """Assert that opted-in public users appear in the email reminder payload."""
    user = configure_public_user_reminders(
        public_client,
        email="public@example.com",
        send_email_reminders=True,
    )
    appointment = create_public_appointment(public_client, seeded_data)
    align_current_pacific_time_for_appointment(
        monkeypatch,
        appointment["start_time"],
        seeded_data["office_timezones"]["limited_office"],
    )

    response = reminder_job_client.get("/appointment/reminders/email/")

    assert_json_response(response, 200)
    assert any(
        item["display_name"] == user["display_name"]
        and item["email"] == "public@example.com"
        for item in json_of(response)["appointments"]
    )


def test_sms_reminders_include_anonymous_phone_appointments(
    internal_ga_client, monkeypatch, reminder_job_client, seeded_data
):
    """Assert that anonymous appointments with a valid phone number appear in SMS reminders."""
    appointment = create_internal_reminder_appointment(
        internal_ga_client,
        seeded_data,
        contact_information="2505550110",
    )
    align_current_pacific_time_for_appointment(
        monkeypatch,
        appointment["start_time"],
        seeded_data["office_timezones"]["test_office"],
    )

    response = reminder_job_client.get("/appointment/reminders/sms/")

    assert_json_response(response, 200)
    assert any(
        item["display_name"] == appointment["citizen_name"]
        and item["user_telephone"] == "2505550110"
        for item in json_of(response)["appointments"]
    )


def test_email_reminders_exclude_public_users_who_did_not_opt_in(
    monkeypatch, public_client, reminder_job_client, seeded_data
):
    """Assert that public users without email opt-in are excluded from reminder delivery."""
    configure_public_user_reminders(
        public_client,
        email="public@example.com",
        send_email_reminders=False,
    )
    appointment = create_public_appointment(public_client, seeded_data)
    align_current_pacific_time_for_appointment(
        monkeypatch,
        appointment["start_time"],
        seeded_data["office_timezones"]["limited_office"],
    )

    response = reminder_job_client.get("/appointment/reminders/email/")

    assert_json_response(response, 200)
    assert json_of(response)["appointments"] == []
