from datetime import datetime, timezone

import pytest
from marshmallow import ValidationError

from app.utilities.timezone_utils import (
    local_datetime_to_utc,
    office_local_isoformat,
)


@pytest.mark.parametrize(
    ("local_value", "expected_utc"),
    [
        ("2026-03-07T12:00:00", datetime(2026, 3, 7, 20, tzinfo=timezone.utc)),
        ("2026-03-08T12:00:00", datetime(2026, 3, 8, 19, tzinfo=timezone.utc)),
        ("2026-12-01T12:00:00", datetime(2026, 12, 1, 19, tzinfo=timezone.utc)),
    ],
)
def test_vancouver_uses_permanent_utc_minus_seven_after_march_8(
    local_value, expected_utc
):
    assert local_datetime_to_utc(local_value, "America/Vancouver") == expected_utc


def test_dawson_creek_remains_utc_minus_seven():
    assert local_datetime_to_utc(
        "2026-01-15T12:00:00", "America/Dawson_Creek"
    ) == datetime(2026, 1, 15, 19, tzinfo=timezone.utc)


def test_local_response_value_has_no_offset():
    assert (
        office_local_isoformat(
            datetime(2026, 12, 1, 19, tzinfo=timezone.utc), "America/Vancouver"
        )
        == "2026-12-01T12:00:00"
    )


def test_aware_input_is_rejected():
    with pytest.raises(ValidationError, match="without a UTC offset"):
        local_datetime_to_utc("2026-12-01T19:00:00Z", "America/Vancouver")


@pytest.mark.parametrize(
    "value",
    ["not-a-date", "2026-02-30T09:00:00", "2026-12-01", "", None, 123, True, [], {}],
)
def test_malformed_local_values_raise_validation_errors(value):
    with pytest.raises(ValidationError):
        local_datetime_to_utc(value, "America/Vancouver")


def test_scheduling_conversion_is_atomic_and_reports_field():
    from app.utilities.timezone_utils import convert_local_fields_to_utc

    payload = {"start_time": "2026-12-01T09:00:00", "end_time": "bad"}
    original = payload.copy()
    with pytest.raises(ValidationError) as error:
        convert_local_fields_to_utc(payload, "America/Vancouver")
    assert "end_time" in error.value.messages
    assert payload == original


@pytest.mark.parametrize(
    "value,zone",
    [
        ("2026-03-08T02:30:00", "America/Vancouver"),
        ("2025-11-02T01:30:00", "America/Edmonton"),
    ],
)
def test_nonexistent_and_ambiguous_times_are_rejected(value, zone):
    with pytest.raises(ValidationError):
        local_datetime_to_utc(value, zone)


def test_partial_interval_validation_uses_existing_endpoint():
    from types import SimpleNamespace
    from app.utilities.timezone_utils import validate_utc_interval

    existing = SimpleNamespace(
        start_time=datetime(2026, 12, 1, 16, tzinfo=timezone.utc),
        end_time=datetime(2026, 12, 1, 17, tzinfo=timezone.utc),
    )
    with pytest.raises(ValidationError):
        validate_utc_interval({"end_time": "2026-12-01T15:00:00+00:00"}, existing)
    validate_utc_interval({"comments": "unchanged time"}, existing)


@pytest.mark.parametrize(
    "day,zone,start,end",
    [
        (
            "2026-12-01",
            "America/Vancouver",
            "2026-12-01T07:00:00+00:00",
            "2026-12-02T07:00:00+00:00",
        ),
        (
            "2026-12-01",
            "America/Edmonton",
            "2026-12-01T06:00:00+00:00",
            "2026-12-02T06:00:00+00:00",
        ),
        (
            "2026-03-08",
            "America/Vancouver",
            "2026-03-08T08:00:00+00:00",
            "2026-03-09T07:00:00+00:00",
        ),
    ],
)
def test_office_day_boundaries_use_pinned_rules(day, zone, start, end):
    from datetime import date
    from app.utilities.timezone_utils import office_day_utc_bounds

    actual = office_day_utc_bounds(date.fromisoformat(day), zone)
    assert [value.isoformat() for value in actual] == [start, end]


def test_clock_offsets_preserve_transition_in_cached_response():
    from app.utilities.timezone_utils import office_clock_offsets

    periods = office_clock_offsets("America/Vancouver", 2026)

    def offset(instant):
        return next(
            p["offset_seconds"] for p in periods if p["start"] <= instant < p["end"]
        )

    assert offset("2026-03-08T09:59:59+00:00") == -8 * 3600
    assert offset("2026-03-08T10:00:00+00:00") == -7 * 3600
    assert offset("2026-12-01T16:00:00+00:00") == -7 * 3600
    assert offset("2027-07-15T16:00:00+00:00") == -7 * 3600
