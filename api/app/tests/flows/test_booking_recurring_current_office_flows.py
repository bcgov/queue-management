from __future__ import annotations

from datetime import datetime, timedelta, timezone
from uuid import uuid4

import pytest

pytestmark = [pytest.mark.flows, pytest.mark.usefixtures("seeded_database")]


def _freeze_recurring_delete_today(monkeypatch, frozen_today: datetime):
    from app.resources.bookings.booking import (
        booking_recurring_stat_delete as recurring_delete_module,
    )

    class FrozenDateTime(datetime):
        @classmethod
        def today(cls):
            return frozen_today

    monkeypatch.setattr(recurring_delete_module, "datetime", FrozenDateTime)


def _create_booking_occurrence(
    app,
    *,
    office_id: int,
    recurring_uuid: str,
    start_time: datetime,
    booking_name: str,
) -> int:
    with app.app_context():
        from app.models.bookings import Booking
        from qsystem import db

        booking = Booking(
            office_id=office_id,
            room_id=None,
            start_time=start_time,
            end_time=start_time + timedelta(hours=2),
            fees="false",
            booking_name=booking_name,
            booking_contact_information="booking@example.com",
            recurring_uuid=recurring_uuid,
        )
        db.session.add(booking)
        db.session.commit()
        return booking.booking_id


def test_current_office_recurring_delete_preserves_before_5am_rows_and_other_offices(
    internal_ga_client, seeded_data, app, monkeypatch
):
    """Assert that current-office recurring deletes only remove this office's non-exempt future rows."""
    _freeze_recurring_delete_today(monkeypatch, datetime(2024, 7, 10, 12, 0, 0))
    recurring_uuid = str(uuid4())

    same_office_future_id = _create_booking_occurrence(
        app,
        office_id=seeded_data["office_ids"]["test_office"],
        recurring_uuid=recurring_uuid,
        start_time=datetime(2024, 7, 11, 17, 0, tzinfo=timezone.utc),
        booking_name="Delete Me",
    )
    same_office_before_5am_id = _create_booking_occurrence(
        app,
        office_id=seeded_data["office_ids"]["test_office"],
        recurring_uuid=recurring_uuid,
        start_time=datetime(2024, 7, 10, 5, 0, tzinfo=timezone.utc),
        booking_name="Preserve Before 5am",
    )
    other_office_future_id = _create_booking_occurrence(
        app,
        office_id=seeded_data["office_ids"]["victoria"],
        recurring_uuid=recurring_uuid,
        start_time=datetime(2024, 7, 11, 18, 0, tzinfo=timezone.utc),
        booking_name="Other Office",
    )

    response = internal_ga_client.delete(
        f"/bookings/recurring/current-office/{recurring_uuid}"
    )

    assert response.status_code == 204, response.get_data(as_text=True)

    with app.app_context():
        from app.models.bookings import Booking

        remaining_ids = {
            booking.booking_id
            for booking in Booking.query.filter_by(recurring_uuid=recurring_uuid).all()
        }

    assert same_office_future_id not in remaining_ids
    assert same_office_before_5am_id in remaining_ids
    assert other_office_future_id in remaining_ids
