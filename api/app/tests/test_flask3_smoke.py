import inspect
from types import SimpleNamespace


def _unwrap(func):
    return inspect.unwrap(func)


def test_routes_command_lists_admin_and_healthz(cli_runner):
    result = cli_runner.invoke(args=["routes"])

    assert result.exit_code == 0, result.output
    assert "/admin/" in result.output
    assert "/api/v1/healthz/" in result.output


def test_admin_index_renders_without_bootstrap3_assets(client):
    response = client.get("/admin/")

    assert response.status_code == 200

    body = response.get_data(as_text=True)

    assert "Admin Console" in body
    assert "bootstrap3" not in body


def test_login_resource_redirects_authenticated_users_to_admin(app, monkeypatch):
    from app.resources.theq import login as login_module

    fake_csr = SimpleNamespace(username="tester")
    logged_in = []

    monkeypatch.setattr(login_module, "get_username", lambda: "tester@idir")
    monkeypatch.setattr(login_module.CSR, "find_by_username", lambda username: fake_csr)
    monkeypatch.setattr(login_module, "login_user", lambda user: logged_in.append(user))

    handler = _unwrap(login_module.Login.get)

    with app.test_request_context("/api/v1/login/"):
        response = handler(login_module.Login())

    assert logged_in == [fake_csr]
    assert response.status_code == 302
    assert response.location.endswith("/admin/")


def test_join_room_handler_emits_success_for_authenticated_csr(app, monkeypatch):
    del app

    from app.resources.theq import websocket

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
