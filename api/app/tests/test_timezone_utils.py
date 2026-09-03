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
    assert office_local_isoformat(
        datetime(2026, 12, 1, 19, tzinfo=timezone.utc), "America/Vancouver"
    ) == "2026-12-01T12:00:00"


def test_aware_input_is_rejected():
    with pytest.raises(ValidationError, match="without a UTC offset"):
        local_datetime_to_utc("2026-12-01T19:00:00Z", "America/Vancouver")
