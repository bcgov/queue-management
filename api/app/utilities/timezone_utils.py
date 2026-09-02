"""Timezone helpers backed by the application's pinned IANA database."""

from datetime import datetime, timezone
from functools import lru_cache
from importlib.resources import files
from zoneinfo import ZoneInfo

from dateutil.parser import parse
from marshmallow import ValidationError


UTC = timezone.utc


@lru_cache(maxsize=None)
def get_timezone(timezone_name: str) -> ZoneInfo:
    """Return a zone from the application's pinned tzdata package."""
    zone_path = files("tzdata.zoneinfo").joinpath(*timezone_name.split("/"))
    with zone_path.open("rb") as zone_file:
        return ZoneInfo.from_file(zone_file, key=timezone_name)


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


def local_datetime_to_utc(value: str | datetime, timezone_name: str) -> datetime:
    """Interpret an offset-less office wall time and return the UTC instant."""
    parsed = parse(value) if isinstance(value, str) else value
    if parsed.tzinfo is not None:
        raise ValidationError("Must be an office-local datetime without a UTC offset.")
    return localize(parsed, timezone_name).astimezone(UTC)


def convert_local_fields_to_utc(data: dict, timezone_name: str) -> dict:
    """Convert scheduling fields in a request payload from office time to UTC."""
    for field_name in ("start_time", "end_time"):
        if data.get(field_name) not in (None, ""):
            data[field_name] = local_datetime_to_utc(data[field_name], timezone_name).isoformat()
    return data


def office_local_isoformat(value: datetime | None, timezone_name: str) -> str | None:
    """Serialize a UTC instant as an offset-less office-local wall time."""
    if value is None:
        return None
    return as_utc(value).astimezone(get_timezone(timezone_name)).replace(tzinfo=None).isoformat()
