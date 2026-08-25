"""Timezone helpers built on Python's stdlib zoneinfo support."""

from datetime import datetime, timezone
from zoneinfo import ZoneInfo


UTC = timezone.utc


def get_timezone(timezone_name: str) -> ZoneInfo:
    """Return a ZoneInfo instance for the given timezone name."""
    return ZoneInfo(timezone_name)


def localize(value: datetime, timezone_name: str) -> datetime:
    """Attach a timezone to a naive datetime or convert an aware datetime."""
    zone = get_timezone(timezone_name)
    if value.tzinfo is None:
        return value.replace(tzinfo=zone)
    return value.astimezone(zone)


def as_utc(value: datetime) -> datetime:
    """Attach UTC to a naive datetime or convert an aware datetime to UTC."""
    if value.tzinfo is None:
        return value.replace(tzinfo=UTC)
    return value.astimezone(UTC)
