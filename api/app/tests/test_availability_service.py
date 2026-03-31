from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, time, timedelta, timezone
import importlib
from zoneinfo import ZoneInfo

import pytest
from app.utilities.yesno import YesNo

pytestmark = [pytest.mark.flows, pytest.mark.integration]


@dataclass
class FakeTimezone:
    timezone_name: str


@dataclass
class FakeTimeslot:
    day_of_week: list[str]
    start_time: time
    end_time: time
    no_of_slots: int


@dataclass
class FakeService:
    is_dlkt: object = None
    timeslot_duration: int | None = None


@dataclass
class FakeOffice:
    office_id: int
    timezone: FakeTimezone
    timeslots: list[FakeTimeslot]
    appointments_enabled_ind: int = 1
    appointment_duration: int = 30
    soonest_appointment: int = 0
    number_of_dlkt: int = 0


@dataclass
class FakeAppointment:
    start_time: datetime
    end_time: datetime
    blackout_flag: str = "N"
    stat_flag: bool = False
    service: FakeService | None = None


def _freeze_now(monkeypatch, frozen_now: datetime):
    availability_module = importlib.import_module("app.services.availability_service")

    class FrozenDateTime(datetime):
        @classmethod
        def now(cls, tz=None):
            if tz is None:
                return frozen_now
            return frozen_now.astimezone(tz)

    monkeypatch.setattr(availability_module.datetime, "datetime", FrozenDateTime)


def _patch_appointments(monkeypatch, appointments: list[FakeAppointment]):
    availability_module = importlib.import_module("app.services.availability_service")
    monkeypatch.setattr(
        availability_module.Appointment,
        "find_appointment_availability",
        lambda **kwargs: appointments,
    )


def _local_day(year: int, month: int, day: int, timezone_name: str) -> datetime:
    return datetime(year, month, day, tzinfo=ZoneInfo(timezone_name))


def _office(
    *,
    timezone_name: str = "America/Vancouver",
    day_names: list[str] | None = None,
    start_hour: int = 9,
    end_hour: int = 12,
    no_of_slots: int = 1,
    appointment_duration: int = 30,
    soonest_appointment: int = 0,
    number_of_dlkt: int = 0,
) -> FakeOffice:
    if day_names is None:
        day_names = ["Wednesday"]
    return FakeOffice(
        office_id=1,
        timezone=FakeTimezone(timezone_name),
        timeslots=[
            FakeTimeslot(
                day_of_week=day_names,
                start_time=time(start_hour, 0),
                end_time=time(end_hour, 0),
                no_of_slots=no_of_slots,
            )
        ],
        appointment_duration=appointment_duration,
        soonest_appointment=soonest_appointment,
        number_of_dlkt=number_of_dlkt,
    )


def test_group_appointments_keeps_local_times_across_dst_boundaries(app):
    """Assert that grouped appointment rows preserve local wall-clock times across DST changes."""
    del app
    AvailabilityService = importlib.import_module(
        "app.services.availability_service"
    ).AvailabilityService
    appointments = [
        FakeAppointment(
            start_time=datetime(2024, 3, 10, 9, 30, tzinfo=timezone.utc),
            end_time=datetime(2024, 3, 10, 10, 0, tzinfo=timezone.utc),
        ),
        FakeAppointment(
            start_time=datetime(2024, 3, 10, 10, 30, tzinfo=timezone.utc),
            end_time=datetime(2024, 3, 10, 11, 0, tzinfo=timezone.utc),
        ),
    ]

    grouped = AvailabilityService.group_appointments(appointments, "America/Vancouver")

    assert "03/10/2024" in grouped
    assert [slot["start_time"].strftime("%H:%M") for slot in grouped["03/10/2024"]] == [
        "01:30",
        "03:30",
    ]


def test_get_available_slots_respects_soonest_appointment_cutoffs(app, monkeypatch):
    """Assert that slots earlier than the office soonest-appointment window are suppressed."""
    del app
    AvailabilityService = importlib.import_module(
        "app.services.availability_service"
    ).AvailabilityService
    _freeze_now(monkeypatch, datetime(2024, 7, 10, 9, 0, tzinfo=timezone.utc))
    _patch_appointments(monkeypatch, [])

    office = _office(timezone_name="UTC", soonest_appointment=90)
    slots = AvailabilityService.get_available_slots(
        office,
        [_local_day(2024, 7, 10, office.timezone.timezone_name)],
    )

    assert [slot["start_time"] for slot in slots["07/10/2024"]] == [
        "10:30",
        "11:00",
        "11:30",
    ]


def test_get_available_slots_prunes_blackout_rows(app, monkeypatch):
    """Assert that blackout appointments remove conflicting slots from the availability map."""
    del app
    AvailabilityService = importlib.import_module(
        "app.services.availability_service"
    ).AvailabilityService
    _freeze_now(monkeypatch, datetime(2024, 7, 10, 8, 0, tzinfo=timezone.utc))
    _patch_appointments(
        monkeypatch,
        [
            FakeAppointment(
                start_time=datetime(2024, 7, 10, 10, 0, tzinfo=timezone.utc),
                end_time=datetime(2024, 7, 10, 10, 30, tzinfo=timezone.utc),
                blackout_flag="Y",
            )
        ],
    )

    office = _office(timezone_name="UTC", end_hour=11, no_of_slots=1)
    slots = AvailabilityService.get_available_slots(
        office,
        [_local_day(2024, 7, 10, office.timezone.timezone_name)],
    )

    assert [slot["start_time"] for slot in slots["07/10/2024"]] == [
        "09:00",
        "09:30",
        "10:30",
    ]


def test_has_available_slots_rejects_overlaps_but_allows_open_following_windows(
    app, monkeypatch
):
    """Assert that conflict checks fail for occupied windows and pass for later open windows."""
    del app
    AvailabilityService = importlib.import_module(
        "app.services.availability_service"
    ).AvailabilityService
    _freeze_now(monkeypatch, datetime(2024, 7, 10, 8, 0, tzinfo=timezone.utc))
    _patch_appointments(
        monkeypatch,
        [
            FakeAppointment(
                start_time=datetime(2024, 7, 10, 9, 0, tzinfo=timezone.utc),
                end_time=datetime(2024, 7, 10, 10, 0, tzinfo=timezone.utc),
            )
        ],
    )

    office = _office(
        timezone_name="UTC", end_hour=11, no_of_slots=1, appointment_duration=60
    )
    service = FakeService()

    blocked = AvailabilityService.has_available_slots(
        office,
        datetime(2024, 7, 10, 9, 30, tzinfo=timezone.utc),
        datetime(2024, 7, 10, 9, 45, tzinfo=timezone.utc),
        service,
    )
    open_window = AvailabilityService.has_available_slots(
        office,
        datetime(2024, 7, 10, 10, 0, tzinfo=timezone.utc),
        datetime(2024, 7, 10, 10, 30, tzinfo=timezone.utc),
        service,
    )

    assert blocked is False
    assert open_window is True


def test_get_available_slots_caps_dlkt_capacity_to_the_office_limit(
    app, monkeypatch
):
    """Assert that DLKT availability honors the office-specific DLKT cap per slot."""
    del app
    AvailabilityService = importlib.import_module(
        "app.services.availability_service"
    ).AvailabilityService
    _freeze_now(monkeypatch, datetime(2024, 7, 10, 8, 0, tzinfo=timezone.utc))
    _patch_appointments(monkeypatch, [])

    office = _office(timezone_name="UTC", no_of_slots=3, number_of_dlkt=1)
    dlkt_service = FakeService(is_dlkt=YesNo.YES)
    slots = AvailabilityService.get_available_slots(
        office,
        [_local_day(2024, 7, 10, office.timezone.timezone_name)],
        service=dlkt_service,
    )

    assert {slot["no_of_slots"] for slot in slots["07/10/2024"]} == {1}
