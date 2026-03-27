from unittest.mock import Mock


def test_sms_endpoint_calls_selected_service(app, client, monkeypatch):
    fake_service = Mock()
    monkeypatch.setattr("api.resources.notifications.get_sms_service", lambda: fake_service)

    payload = [{"user_telephone": "+12505551234", "display_name": "Alex"}]
    response = client.post("/api/v1/notifications/sms", json=payload)

    assert response.status_code == 200
    fake_service.send.assert_called_once_with(payload)


def test_email_endpoint_calls_selected_service(app, client, monkeypatch):
    del app
    fake_service = Mock()
    monkeypatch.setattr("api.resources.email.get_email_service", lambda: fake_service)

    payload = {
        "to": ["citizen@example.com"],
        "subject": "Hello",
        "body": "World",
        "bodyType": "text",
    }
    response = client.post("/api/v1/notifications/email", json=payload)

    assert response.status_code == 200
    fake_service.send.assert_called_once_with(payload)
