from datetime import datetime

import pytest
from app.utilities.date_util import add_delta_to_time, current_pacific_time
from app.utilities.sqlalchemy_compat import utcnow
from app.utilities.timezone_utils import as_utc, get_timezone, localize

pytestmark = pytest.mark.smoke


def test_localize_preserves_dst_offset_for_vancouver():
    """Assert that Vancouver localization keeps the pre-DST offset for naive wall times."""
    localized = localize(datetime(2026, 3, 8, 1, 30), "America/Vancouver")

    assert localized.tzinfo == get_timezone("America/Vancouver")
    assert localized.utcoffset().total_seconds() == -8 * 3600


def test_as_utc_marks_naive_datetimes_as_utc():
    """Assert that naive datetimes are treated as UTC by the compatibility helper."""
    converted = as_utc(datetime(2026, 3, 8, 9, 30))

    assert converted.utcoffset().total_seconds() == 0
    assert converted.isoformat() == "2026-03-08T09:30:00+00:00"


def test_add_delta_to_time_returns_zoneinfo_backed_time():
    """Assert that time arithmetic returns a timezone-aware Vancouver time object."""
    shifted = add_delta_to_time(
        datetime.strptime("08:30", "%H:%M").time(), "America/Vancouver", minutes=30
    )

    assert shifted.strftime("%H:%M") == "09:00"
    assert shifted.tzinfo == get_timezone("America/Vancouver")


def test_current_pacific_time_uses_vancouver_zone():
    """Assert that the Pacific-time helper uses the Vancouver zone definition."""
    pacific_now = current_pacific_time()

    assert pacific_now.tzinfo == get_timezone("America/Vancouver")


def test_utcnow_returns_aware_utc_datetime():
    """Assert that the SQLAlchemy compatibility helper returns an aware UTC datetime."""
    current = utcnow()

    assert current.utcoffset().total_seconds() == 0
    assert current.tzname() == "UTC"
