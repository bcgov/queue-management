from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest
from app.tests.api_test_support import (
    assert_json_response,
    create_draft_appointment,
    create_internal_appointment,
    create_public_draft_and_payload,
    create_public_user,
    json_of,
    public_slot_payload,
    slot_window_to_iso,
)

pytestmark = [pytest.mark.flows, pytest.mark.usefixtures("seeded_database")]


def _appointment_exists(app, appointment_id: int) -> bool:
    with app.app_context():
        from app.models.bookings import Appointment

        return (
            Appointment.query.filter_by(appointment_id=appointment_id).first()
            is not None
        )


def _backdate_appointment(app, appointment_id: int, *, minutes_ago: int) -> None:
    with app.app_context():
        from app.models.bookings import Appointment
        from qsystem import db

        appointment = Appointment.query.filter_by(appointment_id=appointment_id).first()
        appointment.created_at = datetime.now(timezone.utc) - timedelta(
            minutes=minutes_ago
        )
        db.session.add(appointment)
        db.session.commit()


def test_draft_create_persists_is_draft_and_anonymous_fallback_name(
    bare_client, seeded_data, app
):
    """Assert that anonymous draft creation stores the draft flag and the fallback citizen name."""
    payload, _day_key, _slots = public_slot_payload(
        bare_client, seeded_data, minimum_slots=1
    )

    response = bare_client.post("/appointments/draft", json=payload)

    assert_json_response(response, 201)
    appointment = json_of(response)["appointment"]
    assert appointment["is_draft"] is True
    assert appointment["citizen_name"] == "Draft"

    with app.app_context():
        from app.models.bookings import Appointment

        persisted = Appointment.query.filter_by(
            appointment_id=appointment["appointment_id"]
        ).first()
        assert persisted is not None
        assert persisted.is_draft is True
        assert persisted.citizen_name == "Draft"


def test_draft_delete_removes_the_draft_row(bare_client, seeded_data, app):
    """Assert that deleting a draft appointment removes only the draft record from persistence."""
    draft = create_draft_appointment(bare_client, seeded_data)

    response = bare_client.delete(f"/appointments/draft/{draft['appointment_id']}/")

    assert response.status_code == 204, response.get_data(as_text=True)
    assert _appointment_exists(app, draft["appointment_id"]) is False


def test_confirmed_appointment_creation_consumes_the_previous_draft(
    public_client, seeded_data, app
):
    """Assert that creating a confirmed appointment with an appointment_draft_id deletes the draft row."""
    create_public_user(public_client)
    draft, payload = create_public_draft_and_payload(public_client, seeded_data)

    response = public_client.post("/appointments/", json=payload)

    assert_json_response(response, 201)
    appointment = json_of(response)["appointment"]
    assert appointment["is_draft"] is False
    assert _appointment_exists(app, draft["appointment_id"]) is False
    assert _appointment_exists(app, appointment["appointment_id"]) is True


def test_draft_flush_deletes_only_expired_drafts(
    bare_client, internal_ga_client, seeded_data, app
):
    """Assert that draft flushing removes only expired drafts while preserving fresh drafts and confirmed appointments."""
    expired_draft = create_draft_appointment(bare_client, seeded_data)
    payload, day_key, slots = public_slot_payload(
        bare_client, seeded_data, minimum_slots=2
    )
    fresh_start_time, fresh_end_time = slot_window_to_iso(
        day_key,
        slots[1],
        seeded_data["office_timezones"]["limited_office"],
    )
    fresh_response = bare_client.post(
        "/appointments/draft",
        json={
            **payload,
            "start_time": fresh_start_time,
            "end_time": fresh_end_time,
        },
    )
    assert_json_response(fresh_response, 201)
    fresh_draft = json_of(fresh_response)["appointment"]
    confirmed_appointment = create_internal_appointment(
        internal_ga_client, seeded_data, days_from_now=2
    )
    _backdate_appointment(app, expired_draft["appointment_id"], minutes_ago=20)

    response = bare_client.post("/appointments/draft/flush")

    assert_json_response(response, 200)
    deleted_draft_ids = json_of(response)["deleted_draft_ids"]
    assert expired_draft["appointment_id"] in deleted_draft_ids
    assert fresh_draft["appointment_id"] not in deleted_draft_ids
    assert confirmed_appointment["appointment_id"] not in deleted_draft_ids
    assert _appointment_exists(app, expired_draft["appointment_id"]) is False
    assert _appointment_exists(app, fresh_draft["appointment_id"]) is True
    assert _appointment_exists(app, confirmed_appointment["appointment_id"]) is True
