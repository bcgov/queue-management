"""Timezone helpers backed by the application's pinned IANA database."""

import re

from datetime import date, datetime, time, timedelta, timezone
from functools import lru_cache
from importlib.resources import files
from zoneinfo import ZoneInfo

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
    try:
        if isinstance(value, str):
            if not re.fullmatch(
                r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})?",
                value,
            ):
                raise ValueError()
            parsed = datetime.fromisoformat(value)
        elif isinstance(value, datetime):
            parsed = value
        else:
            raise ValueError()
    except (ValueError, TypeError, OverflowError) as error:
        raise ValidationError(
            "Must be a valid office-local datetime (YYYY-MM-DDTHH:mm:ss)."
        ) from error
    if parsed.tzinfo is not None:
        raise ValidationError("Must be an office-local datetime without a UTC offset.")
    localized = localize(parsed, timezone_name)
    result = localized.astimezone(UTC)
    if result.astimezone(localized.tzinfo).replace(tzinfo=None) != parsed:
        raise ValidationError("This local time does not exist in the office time zone.")
    if localized.replace(fold=1).utcoffset() != localized.replace(fold=0).utcoffset():
        raise ValidationError("This local time is ambiguous in the office time zone.")
    return result


def convert_local_fields_to_utc(
    data: dict, timezone_name: str, *, required: bool = False
) -> dict:
    """Convert scheduling fields in a request payload from office time to UTC."""
    if not isinstance(data, dict):
        raise ValidationError("Must be a JSON object.")
    if required:
        missing = {
            name: ["Missing data for required field."]
            for name in ("start_time", "end_time")
            if name not in data
        }
        if missing:
            raise ValidationError(missing)
    converted = {}
    for field_name in ("start_time", "end_time"):
        if field_name in data:
            try:
                converted[field_name] = local_datetime_to_utc(
                    data[field_name], timezone_name
                ).isoformat()
            except ValidationError as error:
                raise ValidationError({field_name: error.messages}) from error
    validate_utc_interval(converted)
    data.update(converted)
    return data


def validate_utc_interval(data: dict, instance=None) -> None:
    """Validate partial edits against persisted endpoints before mutating the row."""
    if not any(name in data for name in ("start_time", "end_time")):
        return
    start = data.get("start_time", getattr(instance, "start_time", None))
    end = data.get("end_time", getattr(instance, "end_time", None))
    if start is not None and end is not None:
        start = datetime.fromisoformat(start) if isinstance(start, str) else start
        end = datetime.fromisoformat(end) if isinstance(end, str) else end
        if as_utc(end) <= as_utc(start):
            raise ValidationError({"end_time": ["Must be after start_time."]})


def office_day_utc_bounds(day: date, timezone_name: str) -> tuple[datetime, datetime]:
    """UTC half-open boundaries for a calendar day, using only pinned rules."""
    zone = get_timezone(timezone_name)
    return (
        datetime.combine(day, time.min, zone).astimezone(UTC),
        datetime.combine(day + timedelta(days=1), time.min, zone).astimezone(UTC),
    )


@lru_cache(maxsize=128)
def office_clock_offsets(timezone_name: str, year: int) -> list[dict]:
    """Clock-only offset periods, including transitions, safe to cache on clients.

    Three calendar years cover long-lived tabs without using browser tzdata.
    Scheduling dates themselves continue to be converted exclusively by the API.
    """
    zone = get_timezone(timezone_name)
    start = datetime(year - 1, 1, 1, tzinfo=UTC)
    end = datetime(year + 2, 1, 1, tzinfo=UTC)

    def offset(instant):
        return int(instant.astimezone(zone).utcoffset().total_seconds())

    periods = [
        {
            "start": start.isoformat(),
            "end": end.isoformat(),
            "offset_seconds": offset(start),
        }
    ]
    cursor = start
    while cursor < end:
        following = min(cursor + timedelta(days=1), end)
        if offset(following) != offset(cursor):
            low, high = int(cursor.timestamp()), int(following.timestamp())
            while high - low > 1:
                middle = (low + high) // 2
                if offset(datetime.fromtimestamp(middle, UTC)) == offset(cursor):
                    low = middle
                else:
                    high = middle
            transition = datetime.fromtimestamp(high, UTC)
            periods[-1]["end"] = transition.isoformat()
            periods.append(
                {
                    "start": transition.isoformat(),
                    "end": end.isoformat(),
                    "offset_seconds": offset(transition),
                }
            )
        cursor = following
    return periods


def office_local_isoformat(value: datetime | None, timezone_name: str) -> str | None:
    """Serialize a UTC instant as an offset-less office-local wall time."""
    if value is None:
        return None
    return (
        as_utc(value)
        .astimezone(get_timezone(timezone_name))
        .replace(tzinfo=None)
        .isoformat()
    )
