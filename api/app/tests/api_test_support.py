from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, time, timedelta, timezone
from typing import Any, Optional
from uuid import uuid4
from zoneinfo import ZoneInfo


@dataclass
class ApiClient:
    client: Any
    identity_name: str
    token: str = "theq-test-token"

    def _normalize_path(self, path: str) -> str:
        if path.startswith("/api/"):
            return path
        if path.startswith("/"):
            return f"/api/v1{path}"
        return f"/api/v1/{path.lstrip('/')}"

    def _headers(self, headers: Optional[dict[str, str]] = None) -> dict[str, str]:
        merged = {
            "Authorization": f"Bearer {self.token}",
            "X-TheQ-Test-Identity": self.identity_name,
        }
        if headers:
            merged.update(headers)
        return merged

    def open(self, path: str, **kwargs):
        headers = self._headers(kwargs.pop("headers", None))
        return self.client.open(self._normalize_path(path), headers=headers, **kwargs)

    def get(self, path: str, **kwargs):
        return self.open(path, method="GET", **kwargs)

    def post(self, path: str, **kwargs):
        return self.open(path, method="POST", **kwargs)

    def put(self, path: str, **kwargs):
        return self.open(path, method="PUT", **kwargs)

    def delete(self, path: str, **kwargs):
        return self.open(path, method="DELETE", **kwargs)


def json_of(response) -> dict[str, Any]:
    return response.get_json()


def assert_status(response, expected_status: int):
    assert response.status_code == expected_status, response.get_data(as_text=True)


def flatten_slots(slots_by_day: dict[str, list[dict[str, Any]]]) -> list[tuple[str, dict[str, Any]]]:
    flattened: list[tuple[str, dict[str, Any]]] = []
    for day, slots in slots_by_day.items():
        for slot in slots:
            flattened.append((day, slot))
    return flattened


def first_day_with_slots(slots_by_day: dict[str, list[dict[str, Any]]], minimum_slots: int = 1) -> tuple[str, list[dict[str, Any]]]:
    for day, slots in slots_by_day.items():
        if len(slots) >= minimum_slots:
            return day, slots
    raise AssertionError(f"expected at least one day with {minimum_slots} slot(s), got {slots_by_day}")


def slot_window_to_iso(day_key: str, slot: dict[str, Any], timezone_name: str) -> tuple[str, str]:
    day_value = datetime.strptime(day_key, "%m/%d/%Y").date()
    timezone = ZoneInfo(timezone_name)
    start_hour, start_minute = [int(part) for part in slot["start_time"].split(":")]
    end_hour, end_minute = [int(part) for part in slot["end_time"].split(":")]
    start_dt = datetime.combine(day_value, time(start_hour, start_minute), tzinfo=timezone)
    end_dt = datetime.combine(day_value, time(end_hour, end_minute), tzinfo=timezone)
    return start_dt.isoformat(), end_dt.isoformat()


def future_utc_window(days_from_now: int, start_hour: int = 17, duration_minutes: int = 30) -> tuple[str, str]:
    start_dt = datetime.now(timezone.utc).replace(microsecond=0, second=0, minute=0, hour=start_hour)
    start_dt = start_dt + timedelta(days=days_from_now)
    end_dt = start_dt + timedelta(minutes=duration_minutes)
    return start_dt.isoformat(), end_dt.isoformat()


def unique_name(prefix: str) -> str:
    return f"{prefix}-{uuid4().hex[:8]}"
