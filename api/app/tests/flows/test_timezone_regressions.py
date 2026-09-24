from datetime import datetime, timedelta, timezone
from uuid import uuid4

import pytest

from app.tests.api_test_support import (
    create_booking,
    create_internal_appointment,
    create_public_user,
    json_of,
)

pytestmark = [pytest.mark.integration, pytest.mark.usefixtures("seeded_database")]


@pytest.mark.parametrize(
    "resource",
    [
        "appointments",
        "bookings",
        "draft",
        "appointment_edit",
        "booking_edit",
        "appointment_series",
        "booking_series",
    ],
)
@pytest.mark.parametrize("bad_value", ["not-a-date", None, 42, "", False])
def test_scheduling_routes_return_field_validation_errors(
    internal_ga_client,
    seeded_data,
    resource,
    bad_value,
):
    client = internal_ga_client
    payload = {
        "office_id": seeded_data["office_ids"]["test_office"],
        "start_time": bad_value,
        "end_time": "2026-12-01T09:30:00",
        "citizen_name": "Timezone QA",
        "booking_name": "Timezone QA",
        "service_id": seeded_data["service_ids"]["msp"],
    }
    method = client.post
    path = f"/{resource}/"
    if resource == "draft":
        path = "/appointments/draft"
    elif resource.endswith("_edit") or resource.endswith("_series"):
        appointment = resource.startswith("appointment")
        kind = "appointments" if appointment else "bookings"
        record = (create_internal_appointment if appointment else create_booking)(
            client, seeded_data, days_from_now=2
        )
        record_id = record["appointment_id" if appointment else "booking_id"]
        method = client.put
        path = f"/{kind}/{record_id}/"
        if resource.endswith("_series"):
            series = str(uuid4())
            assert client.put(path, json={"recurring_uuid": series}).status_code == 200
            path = f"/{kind}/recurring/{series}"
    response = method(path, json=payload)
    assert response.status_code == 422, response.get_data(as_text=True)
    assert "start_time" in json_of(response)["message"]


@pytest.mark.parametrize(
    "creator,kind,id_key",
    [
        (create_booking, "bookings", "booking_id"),
        (create_internal_appointment, "appointments", "appointment_id"),
    ],
)
def test_partial_end_edit_cannot_reverse_interval(
    internal_ga_client, seeded_data, creator, kind, id_key
):
    record = creator(internal_ga_client, seeded_data, days_from_now=2)
    path = f"/{kind}/{record[id_key]}/"
    response = internal_ga_client.put(
        path, json={"end_time": record["local_start_time"]}
    )
    assert response.status_code == 422
    saved = json_of(internal_ga_client.get(path))[
        "booking" if kind == "bookings" else "appointment"
    ]
    assert saved["end_time"] == record["end_time"]


def test_date_queries_use_api_rules_not_postgres_rules(
    app,
    internal_ga_client,
    public_client,
    seeded_data,
    monkeypatch,
):
    """The synthetic zone is deliberately unknown to PostgreSQL."""
    from app.models.bookings import Appointment
    from app.models.theq import Citizen, Office, Timezone
    from app.utilities import timezone_utils
    from app.models.bookings import appointments as model
    from qsystem import db

    user = create_public_user(public_client)
    records = [
        create_internal_appointment(internal_ga_client, seeded_data, days_from_now=2)
        for _ in range(4)
    ]
    ids = {record["appointment_id"] for record in records}
    original_timezone = timezone_utils.get_timezone

    def pinned_zone(name):
        return original_timezone("America/Vancouver" if name == "QA/APIOnly" else name)

    monkeypatch.setattr(timezone_utils, "get_timezone", pinned_zone)
    monkeypatch.setattr(model, "get_timezone", pinned_zone)
    monkeypatch.setattr(
        model,
        "current_pacific_time",
        lambda: datetime(2026, 11, 30, 20, tzinfo=timezone.utc),
    )

    with app.app_context():
        office_id = seeded_data["office_ids"]["test_office"]
        zone = Timezone(timezone_name="QA/APIOnly")
        db.session.add(zone)
        db.session.flush()
        db.session.get(Office, office_id).timezone_id = zone.timezone_id
        starts = [
            "2026-12-01T06:59:00+00:00",
            "2026-12-01T07:00:00+00:00",
            "2026-12-02T06:59:00+00:00",
            "2026-12-02T07:00:00+00:00",
        ]
        for record, start in zip(records, starts):
            row = db.session.get(Appointment, record["appointment_id"])
            row.start_time = datetime.fromisoformat(start)
            row.end_time = row.start_time + timedelta(minutes=30)
            db.session.get(Citizen, row.citizen_id).user_id = user["user_id"]
        db.session.commit()
        expected = {records[1]["appointment_id"], records[2]["appointment_id"]}
        day = datetime(2026, 12, 1, 16, tzinfo=timezone.utc)
        available = Appointment.find_appointment_availability(
            office_id, "QA/APIOnly", day, day
        )
        assert {row.appointment_id for row in available} & ids == expected
        duplicates = Appointment.find_by_username_and_office_id(
            office_id, "theq-public-user@bceid", day.isoformat(), "QA/APIOnly"
        )
        assert {row.appointment_id for row in duplicates} & ids == expected
        reminders = Appointment.find_next_day_appointments()
        assert {row[0].appointment_id for row in reminders} & ids == expected


def test_reminders_use_each_offices_tomorrow_at_midnight(
    app,
    internal_ga_client,
    seeded_data,
    monkeypatch,
):
    from app.models.bookings import Appointment
    from app.models.bookings import appointments as model
    from app.models.theq import Office, Timezone
    from qsystem import db

    records = [
        create_internal_appointment(internal_ga_client, seeded_data, days_from_now=2)
        for _ in range(3)
    ]
    monkeypatch.setattr(
        model,
        "current_pacific_time",
        lambda: datetime(2026, 11, 30, 6, 30, tzinfo=timezone.utc),
    )
    with app.app_context():
        vancouver = db.session.get(Office, seeded_data["office_ids"]["test_office"])
        cranbrook = db.session.get(Office, seeded_data["office_ids"]["limited_office"])
        for office, name in [
            (vancouver, "America/Vancouver"),
            (cranbrook, "America/Edmonton"),
        ]:
            zone = Timezone.query.filter_by(timezone_name=name).first()
            if zone is None:
                zone = Timezone(timezone_name=name)
                db.session.add(zone)
                db.session.flush()
            office.timezone_id = zone.timezone_id
        for record, office, start in zip(
            records,
            [vancouver, cranbrook, cranbrook],
            [
                "2026-11-30T16:00:00+00:00",
                "2026-12-01T15:00:00+00:00",
                "2026-11-30T15:00:00+00:00",
            ],
        ):
            row = db.session.get(Appointment, record["appointment_id"])
            row.office_id = office.office_id
            row.start_time = datetime.fromisoformat(start)
            row.end_time = row.start_time + timedelta(minutes=30)
        db.session.commit()
        ids = {record["appointment_id"] for record in records}
        actual = {
            row[0].appointment_id for row in Appointment.find_next_day_appointments()
        } & ids
        assert actual == {records[0]["appointment_id"], records[1]["appointment_id"]}
