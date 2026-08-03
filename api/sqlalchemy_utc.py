"""Compatibility shim for legacy Alembic migrations and local model imports."""

from app.utilities.sqlalchemy_compat import UtcDateTime, utcnow


class sqltypes:
    UtcDateTime = UtcDateTime
