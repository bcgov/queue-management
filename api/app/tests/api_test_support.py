from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, time, timedelta, timezone
from typing import Any, Optional
from uuid import uuid4


@dataclass
class ApiClient:
    client: Any
    identity_name: Optional[str]
    token: Optional[str] = "theq-test-token"

    def _normalize_path(self, path: str) -> str:
        if path.startswith("/api/"):
            return path
        if path.startswith("/"):
            return f"/api/v1{path}"
        return f"/api/v1/{path.lstrip('/')}"

    def _headers(self, headers: Optional[dict[str, str]] = None) -> dict[str, str]:
        merged: dict[str, str] = {}
        if self.token:
            merged["Authorization"] = f"Bearer {self.token}"
        if self.identity_name:
            merged["X-TheQ-Test-Identity"] = self.identity_name
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


def assert_json_response(response, expected_status: int):
    assert_status(response, expected_status)
    content_type = response.headers.get("Content-Type", "")
    assert content_type.startswith("application/json"), content_type


def assert_unauthorized(response):
    assert_status(response, 401)


def assert_forbidden(response):
    assert_status(response, 403)


def assert_not_auth_error(response):
    assert response.status_code not in {401, 403}, response.get_data(as_text=True)


def flatten_slots(
    slots_by_day: dict[str, list[dict[str, Any]]],
) -> list[tuple[str, dict[str, Any]]]:
    flattened: list[tuple[str, dict[str, Any]]] = []
    for day, slots in slots_by_day.items():
        for slot in slots:
            flattened.append((day, slot))
    return flattened


def first_day_with_slots(
    slots_by_day: dict[str, list[dict[str, Any]]], minimum_slots: int = 1
) -> tuple[str, list[dict[str, Any]]]:
    for day, slots in slots_by_day.items():
        if len(slots) >= minimum_slots:
            return day, slots
    raise AssertionError(
        f"expected at least one day with {minimum_slots} slot(s), got {slots_by_day}"
    )


def slot_window_to_iso(
    day_key: str, slot: dict[str, Any], timezone_name: str
) -> tuple[str, str]:
    day_value = datetime.strptime(day_key, "%m/%d/%Y").date()
    start_hour, start_minute = [int(part) for part in slot["start_time"].split(":")]
    end_hour, end_minute = [int(part) for part in slot["end_time"].split(":")]
    start_dt = datetime.combine(day_value, time(start_hour, start_minute))
    end_dt = datetime.combine(day_value, time(end_hour, end_minute))
    return start_dt.isoformat(), end_dt.isoformat()


def future_utc_window(
    days_from_now: int, start_hour: int = 17, duration_minutes: int = 30
) -> tuple[str, str]:
    start_dt = datetime.now(timezone.utc).replace(
        microsecond=0, second=0, minute=0, hour=start_hour
    )
    start_dt = start_dt + timedelta(days=days_from_now)
    end_dt = start_dt + timedelta(minutes=duration_minutes)
    return start_dt.replace(tzinfo=None).isoformat(), end_dt.replace(tzinfo=None).isoformat()


def unique_name(prefix: str) -> str:
    return f"{prefix}-{uuid4().hex[:8]}"


def create_public_user(api_client: ApiClient) -> dict[str, Any]:
    response = api_client.post("/users/")
    assert_json_response(response, 200)
    return json_of(response)[0]


def public_slot_payload(
    api_client: ApiClient,
    seeded_data: dict[str, Any],
    *,
    minimum_slots: int = 1,
    comments: str = "Public appointment",
    citizen_name: str = "Codex Public User",
    contact_information: str = "public@example.com",
) -> tuple[dict[str, Any], str, list[dict[str, Any]]]:
    slots_response = api_client.get(
        f"/offices/{seeded_data['office_ids']['limited_office']}/slots/?service_id={seeded_data['service_ids']['limited_office_service']}"
    )
    assert_json_response(slots_response, 200)
    day_key, slots = first_day_with_slots(
        json_of(slots_response), minimum_slots=minimum_slots
    )
    start_time, end_time = slot_window_to_iso(
        day_key, slots[0], seeded_data["office_timezones"]["limited_office"]
    )
    return (
        {
            "service_id": seeded_data["service_ids"]["limited_office_service"],
            "office_id": seeded_data["office_ids"]["limited_office"],
            "start_time": start_time,
            "end_time": end_time,
            "comments": comments,
            "citizen_name": citizen_name,
            "contact_information": contact_information,
        },
        day_key,
        slots,
    )


def create_draft_appointment(
    api_client: ApiClient,
    seeded_data: dict[str, Any],
    *,
    minimum_slots: int = 1,
) -> dict[str, Any]:
    payload, _day_key, _slots = public_slot_payload(
        api_client, seeded_data, minimum_slots=minimum_slots
    )
    response = api_client.post("/appointments/draft", json=payload)
    assert_json_response(response, 201)
    return json_of(response)["appointment"]


def create_public_draft_and_payload(
    api_client: ApiClient, seeded_data: dict[str, Any]
) -> tuple[dict[str, Any], dict[str, Any]]:
    draft = create_draft_appointment(api_client, seeded_data, minimum_slots=1)
    payload, _day_key, _slots = public_slot_payload(
        api_client, seeded_data, minimum_slots=1
    )
    payload["appointment_draft_id"] = draft["appointment_id"]
    return draft, payload


def create_internal_appointment(
    api_client: ApiClient,
    seeded_data: dict[str, Any],
    *,
    days_from_now: int,
    recurring_uuid: Optional[str] = None,
) -> dict[str, Any]:
    start_time, end_time = future_utc_window(days_from_now)
    response = api_client.post(
        "/appointments/",
        json={
            "service_id": seeded_data["service_ids"]["msp"],
            "office_id": seeded_data["office_ids"]["test_office"],
            "start_time": start_time,
            "end_time": end_time,
            "comments": "Internal appointment",
            "citizen_name": unique_name("internal-appt"),
            "contact_information": "internal@example.com",
            "recurring_uuid": recurring_uuid,
        },
    )
    assert_json_response(response, 201)
    return json_of(response)["appointment"]


def create_booking(
    api_client: ApiClient,
    seeded_data: dict[str, Any],
    *,
    days_from_now: int,
    recurring_uuid: Optional[str] = None,
    invigilator_ids: Optional[list[int]] = None,
    office_id: Optional[int] = None,
    room_id: Optional[int] = None,
    booking_name: Optional[str] = None,
) -> dict[str, Any]:
    start_time, end_time = future_utc_window(days_from_now, duration_minutes=120)
    if invigilator_ids is None:
        invigilator_ids = [seeded_data["invigilator_ids"][0]]
    if office_id is None:
        office_id = seeded_data["office_ids"]["test_office"]
    if room_id is None:
        room_id = seeded_data["room_id"]
    if booking_name is None:
        booking_name = unique_name("booking")
    response = api_client.post(
        "/bookings/",
        json={
            "booking_name": booking_name,
            "booking_contact_information": "booking@example.com",
            "fees": "false",
            "office_id": office_id,
            "room_id": room_id,
            "start_time": start_time,
            "end_time": end_time,
            "recurring_uuid": recurring_uuid,
            "invigilator_id": invigilator_ids,
        },
    )
    assert_json_response(response, 201)
    return json_of(response)["booking"]


def create_exam(
    api_client: ApiClient,
    seeded_data: dict[str, Any],
    booking_id: Optional[int],
    *,
    event_id: str,
    exam_type_id: Optional[int] = None,
    office_id: Optional[int] = None,
    **overrides: Any,
) -> dict[str, Any]:
    expiry_date = (
        (datetime.now(timezone.utc) + timedelta(days=30))
        .replace(microsecond=0)
        .isoformat()
    )
    payload = {
        "event_id": event_id,
        "exam_method": "paper",
        "exam_name": unique_name("exam"),
        "exam_type_id": (
            seeded_data["exam_type_id"] if exam_type_id is None else exam_type_id
        ),
        "exam_written_ind": 0,
        "examinee_name": "Codex Examinee",
        "notes": "Codex exam notes",
        "number_of_students": 19,
        "office_id": (
            seeded_data["office_ids"]["test_office"]
            if office_id is None
            else office_id
        ),
        "offsite_location": "Test Office",
        "expiry_date": expiry_date,
    }
    if booking_id is not None:
        payload["booking_id"] = booking_id
    payload.update(overrides)
    response = api_client.post(
        "/exams/",
        json=payload,
    )
    assert_json_response(response, 201)
    return json_of(response)["exam"]


def create_citizen(
    api_client: ApiClient,
    position: int,
    *,
    name: str,
    comments: Optional[str] = None,
) -> dict[str, Any]:
    payload = {"citizen_name": name}
    if comments is not None:
        payload["citizen_comments"] = comments

    response = api_client.post(f"/citizens/{position}/add_citizen/", json=payload)
    assert_json_response(response, 201)
    return json_of(response)["citizen"]


def update_citizen(api_client: ApiClient, citizen_id: int, **payload) -> dict[str, Any]:
    response = api_client.put(f"/citizens/{citizen_id}/", json=payload)
    assert_json_response(response, 200)
    return json_of(response)["citizen"]


def create_service_request(
    api_client: ApiClient,
    citizen_id: int,
    *,
    service_id: int,
    channel_id: int,
    quantity: int,
) -> dict[str, Any]:
    response = api_client.post(
        "/service_requests/",
        json={
            "service_request": {
                "citizen_id": citizen_id,
                "service_id": service_id,
                "channel_id": channel_id,
                "quantity": quantity,
            }
        },
    )
    assert_json_response(response, 201)
    return json_of(response)["service_request"]


def create_service_ready_citizen(
    api_client: ApiClient,
    seeded_data: dict[str, Any],
    *,
    position: int,
    name: str,
    service_id_key: str,
    channel_id_key: str,
    quantity: int,
    counter_id_key: Optional[str] = None,
    qt_xn_citizen_ind: Optional[int] = None,
    comments: Optional[str] = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    citizen = create_citizen(api_client, position, name=name, comments=comments)

    update_payload = {"citizen_name": name}
    if comments is not None:
        update_payload["citizen_comments"] = comments
    if counter_id_key is not None:
        update_payload["counter_id"] = seeded_data["counter_ids"][counter_id_key]
    if qt_xn_citizen_ind is not None:
        update_payload["qt_xn_citizen_ind"] = qt_xn_citizen_ind

    updated = update_citizen(api_client, citizen["citizen_id"], **update_payload)
    service_request = create_service_request(
        api_client,
        updated["citizen_id"],
        service_id=seeded_data["service_ids"][service_id_key],
        channel_id=seeded_data["channel_ids"][channel_id_key],
        quantity=quantity,
    )
    return updated, service_request


def create_queue_ready_citizen(
    api_client: ApiClient,
    seeded_data: dict[str, Any],
    *,
    position: int,
    name: str,
    service_id_key: str,
    channel_id_key: str,
    quantity: int,
    counter_id_key: str,
    qt_xn_citizen_ind: int,
    comments: Optional[str] = None,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    citizen, service_request = create_service_ready_citizen(
        api_client,
        seeded_data,
        position=position,
        name=name,
        service_id_key=service_id_key,
        channel_id_key=channel_id_key,
        quantity=quantity,
        counter_id_key=counter_id_key,
        qt_xn_citizen_ind=qt_xn_citizen_ind,
        comments=comments,
    )
    queued_response = api_client.post(
        f"/citizens/{citizen['citizen_id']}/add_to_queue/"
    )
    assert_json_response(queued_response, 200)
    return citizen, service_request, json_of(queued_response)["citizen"]
