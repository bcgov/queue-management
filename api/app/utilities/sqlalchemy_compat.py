"""Local SQLAlchemy helpers for UTC-aware datetime columns."""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import DateTime
from sqlalchemy.types import TypeDecorator


UTC = timezone.utc


class UtcDateTime(TypeDecorator):
    """Store datetimes in UTC and always return aware UTC values."""

    impl = DateTime
    cache_ok = True

    def __init__(self, *args, timezone: bool = True, **kwargs):
        super().__init__(*args, **kwargs)
        self.timezone = timezone

    def load_dialect_impl(self, dialect):
        return dialect.type_descriptor(DateTime(timezone=self.timezone))

    def process_bind_param(self, value, dialect):
        del dialect
        if value is None:
            return None
        if value.tzinfo is None:
            return value.replace(tzinfo=UTC)
        return value.astimezone(UTC)

    def process_result_value(self, value, dialect):
        del dialect
        if value is None:
            return None
        if value.tzinfo is None:
            return value.replace(tzinfo=UTC)
        return value.astimezone(UTC)


def utcnow() -> datetime:
    """Return the current UTC time as an aware datetime."""

    return datetime.now(UTC)
