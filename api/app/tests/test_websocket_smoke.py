import inspect
from types import SimpleNamespace

import pytest


def _unwrap(func):
    return inspect.unwrap(func)


def _import_websocket(monkeypatch):
    class Response:
        def read(self):
            return (
                b'{"jwks_uri":"https://example.com/jwks.json","issuer":"https://example.com/"}'
            )

    monkeypatch.setattr(
        "flask_jwt_oidc.jwt_manager.urlopen",
        lambda url: Response(),
    )

    from app.resources.theq import websocket

    return websocket


pytestmark = pytest.mark.smoke


def test_join_room_handler_emits_success_for_authenticated_csr(monkeypatch):
    """Assert that websocket room joins still emit the expected success events."""
    websocket = _import_websocket(monkeypatch)

    joined_rooms = []
    emitted_events = []
    fake_csr = SimpleNamespace(
        username="tester",
        office=SimpleNamespace(office_name="Victoria"),
    )

    monkeypatch.setattr(websocket, "get_username", lambda: "tester@idir")
    monkeypatch.setattr(websocket.CSR, "find_by_username", lambda username: fake_csr)
    monkeypatch.setattr(websocket, "join_room", lambda room: joined_rooms.append(room))
    monkeypatch.setattr(
        websocket,
        "emit",
        lambda event, payload=None: emitted_events.append((event, payload)),
    )
    monkeypatch.setattr(websocket, "request", SimpleNamespace(sid="socket-1"))

    handler = _unwrap(websocket.on_join)
    handler({})

    assert joined_rooms == ["Victoria"]
    assert emitted_events == [
        ("joinRoomSuccess", {"sucess": True}),
        ("get_Csr_State_IDs", {"success": True}),
        ("update_customer_list", {"success": True}),
    ]


def test_join_room_handler_fails_without_a_username(monkeypatch):
    """Assert that joinRoom fails cleanly when no authenticated username is present."""
    websocket = _import_websocket(monkeypatch)

    emitted_events = []

    monkeypatch.setattr(websocket, "get_username", lambda: "")
    monkeypatch.setattr(
        websocket,
        "emit",
        lambda event, payload=None: emitted_events.append((event, payload)),
    )

    handler = _unwrap(websocket.on_join)
    handler({})

    assert emitted_events == [("joinRoomFail", {"success": False})]


def test_join_room_handler_fails_when_csr_lookup_misses(monkeypatch):
    """Assert that joinRoom fails when the username does not resolve to a CSR."""
    websocket = _import_websocket(monkeypatch)

    emitted_events = []

    monkeypatch.setattr(websocket, "get_username", lambda: "missing@idir")
    monkeypatch.setattr(websocket.CSR, "find_by_username", lambda username: None)
    monkeypatch.setattr(
        websocket,
        "emit",
        lambda event, payload=None: emitted_events.append((event, payload)),
    )

    handler = _unwrap(websocket.on_join)
    handler({})

    assert emitted_events == [("joinRoomFail", {"success": False})]


def test_join_smartboard_room_success_joins_the_expected_room(monkeypatch):
    """Assert that smartboard room joins use the office-scoped socket room name."""
    websocket = _import_websocket(monkeypatch)

    joined_rooms = []
    emitted_events = []

    monkeypatch.setattr(websocket, "join_room", lambda room: joined_rooms.append(room))
    monkeypatch.setattr(
        websocket,
        "emit",
        lambda event, payload=None: emitted_events.append((event, payload)),
    )
    monkeypatch.setattr(websocket, "request", SimpleNamespace(sid="socket-2"))

    websocket.on_join_smartboard({"office_id": "7"})

    assert joined_rooms == ["sb-7"]
    assert emitted_events == [("joinSmartboardRoomSuccess", None)]


def test_join_smartboard_room_rejects_missing_office_id(monkeypatch):
    """Assert that smartboard joins fail with a clear message when office_id is missing."""
    websocket = _import_websocket(monkeypatch)

    emitted_events = []

    monkeypatch.setattr(
        websocket,
        "emit",
        lambda event, payload=None: emitted_events.append((event, payload)),
    )

    websocket.on_join_smartboard({})

    assert emitted_events == [
        (
            "joinSmartboardRoomFail",
            {"sucess": False, "message": "office_id must be passed to this method"},
        )
    ]


def test_join_smartboard_room_rejects_non_integer_office_id(monkeypatch):
    """Assert that smartboard joins fail when office_id is not numeric."""
    websocket = _import_websocket(monkeypatch)

    emitted_events = []

    monkeypatch.setattr(
        websocket,
        "emit",
        lambda event, payload=None: emitted_events.append((event, payload)),
    )

    websocket.on_join_smartboard({"office_id": "abc"})

    assert emitted_events == [
        (
            "joinSmartboardRoomFail",
            {"sucess": False, "message": "office_id must be an integer"},
        )
    ]


def test_clear_csr_user_id_updates_the_csr_cache(monkeypatch):
    """Assert that the clear-cache websocket event delegates to CSR.update_user_cache."""
    websocket = _import_websocket(monkeypatch)

    updated_ids = []

    monkeypatch.setattr(
        websocket.CSR, "update_user_cache", lambda csr_id: updated_ids.append(csr_id)
    )

    websocket.clear_csr_user_id(42)

    assert updated_ids == [42]


def test_sync_offices_cache_clears_the_office_cache(monkeypatch):
    """Assert that office cache sync delegates to Office.clear_offices_cache."""
    websocket = _import_websocket(monkeypatch)

    calls = []

    monkeypatch.setattr(
        websocket.Office, "clear_offices_cache", lambda: calls.append("cleared")
    )

    websocket.sync_offices_cache()

    assert calls == ["cleared"]
