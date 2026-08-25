from __future__ import annotations

import re
from datetime import datetime, timedelta, timezone

import pytest
from app.tests.api_test_support import (
    assert_json_response,
    create_queue_ready_citizen,
    json_of,
)
from app.tests.auth.auth_support import create_walkin_target

pytestmark = [pytest.mark.flows, pytest.mark.usefixtures("seeded_database")]


def _configure_office(
    app,
    office_id: int,
    *,
    currently_waiting: int | None = None,
    automatic_reminder_at: int | None = None,
) -> int:
    with app.app_context():
        from app.models.theq import Office
        from qsystem import db

        office = Office.find_by_id(office_id)
        if currently_waiting is not None:
            office.currently_waiting = currently_waiting
        if automatic_reminder_at is not None:
            office.automatic_reminder_at = automatic_reminder_at
        db.session.add(office)
        db.session.commit()
        return office.office_number


def _insert_current_agenda_panel_appointment(app, seeded_data) -> int:
    with app.app_context():
        from app.models.bookings import Appointment
        from qsystem import db

        start_time = datetime.now(timezone.utc).replace(microsecond=0) + timedelta(
            minutes=5
        )
        appointment = Appointment(
            office_id=seeded_data["office_ids"]["test_office"],
            service_id=seeded_data["service_ids"]["ptax"],
            start_time=start_time,
            end_time=start_time + timedelta(minutes=30),
            citizen_name="Agenda Panel Citizen",
            contact_information="agenda@example.com",
            blackout_flag="N",
            is_draft=False,
            stat_flag=False,
        )
        db.session.add(appointment)
        db.session.commit()
        return appointment.appointment_id


def _configure_walkin_citizen(
    app,
    citizen_id: int,
    *,
    notification_phone: str | None = None,
    notification_email: str | None = None,
    start_position: int | None = None,
    start_time: datetime | None = None,
):
    with app.app_context():
        from app.models.theq import Citizen
        from qsystem import db

        citizen = Citizen.find_citizen_by_id(citizen_id)
        if notification_phone is not None:
            citizen.notification_phone = notification_phone
        if notification_email is not None:
            citizen.notification_email = notification_email
        if start_position is not None:
            citizen.start_position = start_position
        if start_time is not None:
            citizen.start_time = start_time
        db.session.add(citizen)
        db.session.commit()


def _place_citizen_on_hold(internal_ga_client, citizen_id: int):
    begin_response = internal_ga_client.post(f"/citizens/{citizen_id}/begin_service/")
    hold_response = internal_ga_client.post(f"/citizens/{citizen_id}/place_on_hold/")
    assert_json_response(begin_response, 200)
    assert_json_response(hold_response, 200)


def test_walkin_lookup_groups_booked_agenda_and_walkin_entries(
    bare_client, internal_ga_client, seeded_data, app
):
    """Assert that walk-in lookups keep booked, agenda, and walk-in entries in frontend order."""
    create_queue_ready_citizen(
        internal_ga_client,
        seeded_data,
        position=0,
        name="Booked Queue Citizen",
        service_id_key="ptax",
        channel_id_key="phone",
        quantity=1,
        counter_id_key="counter",
        qt_xn_citizen_ind=0,
        comments="booked|||appointment",
    )
    target_citizen, walkin_id = create_walkin_target(
        app, internal_ga_client, seeded_data
    )
    _insert_current_agenda_panel_appointment(app, seeded_data)

    response = bare_client.get(f"/citizen/all-walkin/{walkin_id}/")
    body = json_of(response)

    assert_json_response(response, 200)
    assert [entry["flag"] for entry in body["citizen"]] == [
        "booked_app",
        "agenda_panel",
        "walkin_app",
    ]
    assert body["citizen"][0]["ticket_number"]
    assert re.fullmatch(
        r"\d{2}/\d{2}/\d{4}, \d{2}:\d{2}:\d{2}", body["citizen"][1]["start_time"]
    )
    assert body["citizen"][2]["walkin_unique_id"] == walkin_id
    assert body["show_estimate"] in {True, False}
    assert target_citizen["citizen_id"] > 0


def test_waiting_queue_details_group_booked_and_walkin_rows(
    bare_client, internal_ga_client, seeded_data, app
):
    """Assert that waiting queue details preserve the booked-then-walkin grouping the smartboard renders."""
    create_queue_ready_citizen(
        internal_ga_client,
        seeded_data,
        position=0,
        name="Booked Queue Citizen",
        service_id_key="ptax",
        channel_id_key="phone",
        quantity=1,
        counter_id_key="counter",
        qt_xn_citizen_ind=0,
        comments="booked|||appointment",
    )
    walkin_citizen, _walkin_id = create_walkin_target(app, internal_ga_client, seeded_data)
    office_number = _configure_office(
        app, seeded_data["office_ids"]["test_office"], currently_waiting=1
    )

    response = bare_client.get(f"/smardboard/Q-details/waiting/{office_number}")
    body = json_of(response)

    assert_json_response(response, 200)
    assert [entry["flag"] for entry in body["citizen_in_q"]] == [
        "booked_app",
        "walkin_app",
    ]
    assert body["citizen_in_q"][0]["service_name"] == "Property Tax"
    assert body["citizen_in_q"][1]["citizen_id"] == walkin_citizen["citizen_id"]


def test_upcoming_queue_details_return_localized_agenda_panel_rows(
    bare_client, seeded_data, app
):
    """Assert that upcoming queue details expose agenda-panel rows in display-ready format."""
    office_number = _configure_office(
        app, seeded_data["office_ids"]["test_office"], currently_waiting=1
    )
    _insert_current_agenda_panel_appointment(app, seeded_data)

    response = bare_client.get(f"/smardboard/Q-details/upcoming/{office_number}")
    body = json_of(response)

    assert_json_response(response, 200)
    assert len(body["booked_not_checkin"]) == 1
    assert body["booked_not_checkin"][0]["flag"] == "agenda_panel"
    assert re.fullmatch(
        r"\d{2}/\d{2}/\d{4}, \d{2}:\d{2}:\d{2}",
        body["booked_not_checkin"][0]["start_time"],
    )


def test_smartboard_returns_waiting_tickets_and_active_periods(
    bare_client, internal_ga_client, seeded_data, app
):
    """Assert that the public smartboard response carries ticket numbers and waiting-state periods."""
    _citizen, _service_request, queued_citizen = create_queue_ready_citizen(
        internal_ga_client,
        seeded_data,
        position=0,
        name="Smartboard Citizen",
        service_id_key="ptax",
        channel_id_key="phone",
        quantity=1,
        counter_id_key="counter",
        qt_xn_citizen_ind=0,
    )
    office_number = _configure_office(
        app, seeded_data["office_ids"]["test_office"], currently_waiting=1
    )

    response = bare_client.get(f"/smartboard/?office_number={office_number}")
    body = json_of(response)

    assert_json_response(response, 200)
    waiting_entry = next(
        citizen
        for citizen in body["citizens"]
        if citizen["ticket_number"] == queued_citizen["ticket_number"]
    )
    assert waiting_entry["active_period"]["ps"]["ps_name"] == "Waiting"


def test_send_line_walkin_reminder_updates_notification_flags(
    internal_ga_client, seeded_data, app, monkeypatch
):
    """Assert that walk-in reminders flip the persisted reminder flags once the SMS path runs."""
    from app.resources.bookings.walkin import walkin as walkin_module

    monkeypatch.setattr(
        walkin_module, "send_walkin_reminder_sms", lambda *args, **kwargs: True
    )
    walkin_citizen, _walkin_id = create_walkin_target(
        app, internal_ga_client, seeded_data
    )
    _configure_office(
        app,
        seeded_data["office_ids"]["test_office"],
        automatic_reminder_at=1,
    )

    response = internal_ga_client.post(
        "/send-reminder/line-walkin/",
        json={"previous_citizen_id": walkin_citizen["citizen_id"]},
    )

    assert_json_response(response, 200)

    with app.app_context():
        from app.models.theq import Citizen

        citizen = Citizen.find_citizen_by_id(walkin_citizen["citizen_id"])
        assert citizen.automatic_reminder_flag == 1
        assert citizen.reminder_flag == 1
        assert citizen.notification_sent_time is not None


def test_walkin_lookup_includes_later_walkins_when_the_target_citizen_is_on_hold(
    bare_client, internal_ga_client, seeded_data, app
):
    """Assert that on-hold citizens continue to see later walk-ins in the lookup payload."""
    target_citizen, walkin_id = create_walkin_target(app, internal_ga_client, seeded_data)
    later_citizen, later_walkin_id = create_walkin_target(
        app, internal_ga_client, seeded_data
    )
    _configure_walkin_citizen(
        app,
        later_citizen["citizen_id"],
        start_time=datetime.now(timezone.utc) + timedelta(minutes=30),
    )

    initial_response = bare_client.get(f"/citizen/all-walkin/{walkin_id}/")
    initial_walkin_ids = {
        entry.get("walkin_unique_id")
        for entry in json_of(initial_response)["citizen"]
        if entry.get("flag") == "walkin_app"
    }
    assert later_walkin_id not in initial_walkin_ids

    _place_citizen_on_hold(internal_ga_client, target_citizen["citizen_id"])
    held_response = bare_client.get(f"/citizen/all-walkin/{walkin_id}/")
    held_walkin_ids = {
        entry.get("walkin_unique_id")
        for entry in json_of(held_response)["citizen"]
        if entry.get("flag") == "walkin_app"
    }

    assert_json_response(held_response, 200)
    assert later_citizen["citizen_id"] > 0
    assert later_walkin_id in held_walkin_ids


def test_send_line_walkin_reminder_skips_notifications_before_the_threshold_position(
    internal_ga_client, seeded_data, app, monkeypatch
):
    """Assert that reminder side effects stay off until a citizen reaches the configured threshold."""
    first_citizen, _first_walkin_id = create_walkin_target(app, internal_ga_client, seeded_data)
    second_citizen, _second_walkin_id = create_walkin_target(
        app, internal_ga_client, seeded_data
    )
    _configure_walkin_citizen(app, second_citizen["citizen_id"], start_position=1)
    _configure_office(
        app,
        seeded_data["office_ids"]["test_office"],
        automatic_reminder_at=2,
    )

    monkeypatch.setattr(
        "app.resources.bookings.walkin.walkin.send_walkin_reminder_sms",
        lambda *args, **kwargs: (_ for _ in ()).throw(
            AssertionError("SMS reminder should not have been sent")
        ),
    )
    monkeypatch.setattr(
        "app.resources.bookings.walkin.walkin.send_email",
        lambda *args, **kwargs: (_ for _ in ()).throw(
            AssertionError("Email reminder should not have been sent")
        ),
    )

    response = internal_ga_client.post(
        "/send-reminder/line-walkin/",
        json={"previous_citizen_id": first_citizen["citizen_id"]},
    )

    assert_json_response(response, 200)

    with app.app_context():
        from app.models.theq import Citizen

        refreshed = Citizen.find_citizen_by_id(second_citizen["citizen_id"])
        assert refreshed.automatic_reminder_flag in {None, 0}
        assert refreshed.reminder_flag in {None, 0}
        assert refreshed.notification_sent_time is None


def test_send_line_walkin_reminder_uses_email_when_no_phone_number_is_available(
    internal_ga_client, seeded_data, app, monkeypatch
):
    """Assert that the email reminder branch updates the persisted flags when SMS is unavailable."""
    email_calls = []
    monkeypatch.setattr(
        "app.resources.bookings.walkin.walkin.get_walkin_reminder_email_contents",
        lambda citizen, office: ("walkin@example.com", "Reminder", "Body"),
    )
    monkeypatch.setattr(
        "app.resources.bookings.walkin.walkin.send_email",
        lambda token, *args: email_calls.append((token, args)),
    )

    walkin_citizen, _walkin_id = create_walkin_target(
        app, internal_ga_client, seeded_data
    )
    _configure_walkin_citizen(
        app,
        walkin_citizen["citizen_id"],
        notification_phone="",
        notification_email="walkin@example.com",
        start_position=1,
    )
    _configure_office(
        app,
        seeded_data["office_ids"]["test_office"],
        automatic_reminder_at=1,
    )

    response = internal_ga_client.post(
        "/send-reminder/line-walkin/",
        json={"previous_citizen_id": walkin_citizen["citizen_id"]},
    )

    assert_json_response(response, 200)
    assert len(email_calls) == 1
    assert email_calls[0][0] == "theq-test-token"

    with app.app_context():
        from app.models.theq import Citizen

        citizen = Citizen.find_citizen_by_id(walkin_citizen["citizen_id"])
        assert citizen.automatic_reminder_flag == 1
        assert citizen.reminder_flag == 1
        assert citizen.notification_sent_time is not None
