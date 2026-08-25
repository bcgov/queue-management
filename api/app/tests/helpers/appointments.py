from __future__ import annotations

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from app.tests.api_test_support import (
    assert_json_response,
    create_public_user,
    future_utc_window,
    json_of,
    unique_name,
)


def align_current_pacific_time_for_appointment(
    monkeypatch, appointment_start_time: str, timezone_name: str
):
    appointment_local = datetime.fromisoformat(
        appointment_start_time.replace("Z", "+00:00")
    ).astimezone(ZoneInfo(timezone_name))
    now_local = appointment_local - timedelta(days=1)
    monkeypatch.setattr(
        "app.models.bookings.appointments.current_pacific_time", lambda: now_local
    )


def configure_public_user_reminders(
    public_client,
    *,
    email: str,
    telephone: str | None = None,
    send_email_reminders: bool = False,
    send_sms_reminders: bool = False,
) -> dict:
    user = create_public_user(public_client)
    response = public_client.put(
        f"/users/{user['user_id']}/",
        json={
            "email": email,
            "telephone": telephone,
            "send_email_reminders": send_email_reminders,
            "send_sms_reminders": send_sms_reminders,
        },
    )
    assert_json_response(response, 200)
    return json_of(response)[0]


def create_internal_reminder_appointment(
    api_client,
    seeded_data,
    *,
    contact_information: str,
    days_from_now: int = 2,
    citizen_name: str = "Reminder Appointment",
) -> dict:
    start_time, end_time = future_utc_window(days_from_now)
    response = api_client.post(
        "/appointments/",
        json={
            "service_id": seeded_data["service_ids"]["msp"],
            "office_id": seeded_data["office_ids"]["test_office"],
            "start_time": start_time,
            "end_time": end_time,
            "comments": "Reminder coverage",
            "citizen_name": unique_name(citizen_name),
            "contact_information": contact_information,
        },
    )
    assert_json_response(response, 201)
    return json_of(response)["appointment"]
