def _notification_messages(caplog) -> str:
    """Return combined notification log messages."""
    return "\n".join(
        record.getMessage()
        for record in caplog.records
        if record.name == "api.services.notifications"
    )


def test_sms_endpoint_logs_gc_notify_shaped_payload_for_reminder(app, client, caplog):
    del client
    app.config["SMS_PROVIDER"] = "LOG"
    payload = [{"user_telephone": "+12505551234", "display_name": "Alex"}]

    with app.test_client() as test_client, caplog.at_level(
        "INFO", logger="api.services.notifications"
    ):
        response = test_client.post("/api/v1/notifications/sms", json=payload)

    log_output = _notification_messages(caplog)
    assert response.status_code == 200
    assert '"phone_number": "+12505551234"' in log_output
    assert '"template_id": "sms-template"' in log_output
    assert '"sms_text": "Reminder Alex http://localhost:8081"' in log_output


def test_sms_endpoint_logs_gc_notify_shaped_payload_for_checkin_confirmation(app, client, caplog):
    del client
    app.config["SMS_PROVIDER"] = "LOG"
    payload = [
        {
            "user_telephone": "+12505551234",
            "ticket_number": "A123",
            "type": "CHECKIN_CONFIRMATION",
            "url": "http://localhost:8081/checkin/A123",
        }
    ]

    with app.test_client() as test_client, caplog.at_level(
        "INFO", logger="api.services.notifications"
    ):
        response = test_client.post("/api/v1/notifications/sms", json=payload)

    log_output = _notification_messages(caplog)
    assert response.status_code == 200
    assert '"phone_number": "+12505551234"' in log_output
    assert '"sms_text": "Checkin A123 http://localhost:8081/checkin/A123"' in log_output


def test_sms_endpoint_logs_gc_notify_shaped_payload_for_custom_sms(app, client, caplog):
    del client
    app.config["SMS_PROVIDER"] = "LOG"
    payload = [
        {
            "user_telephone": "+12505551234",
            "type": "CUSTOM",
            "message": "Bring your ID.",
        }
    ]

    with app.test_client() as test_client, caplog.at_level(
        "INFO", logger="api.services.notifications"
    ):
        response = test_client.post("/api/v1/notifications/sms", json=payload)

    log_output = _notification_messages(caplog)
    assert response.status_code == 200
    assert '"phone_number": "+12505551234"' in log_output
    assert '"sms_text": "Bring your ID."' in log_output


def test_sms_endpoint_skips_logging_when_phone_number_is_missing(app, client, caplog):
    del client
    app.config["SMS_PROVIDER"] = "LOG"
    payload = [{"display_name": "Alex"}]

    with app.test_client() as test_client, caplog.at_level(
        "INFO", logger="api.services.notifications"
    ):
        response = test_client.post("/api/v1/notifications/sms", json=payload)

    assert response.status_code == 200
    assert _notification_messages(caplog) == ""


def test_email_endpoint_logs_gc_notify_shaped_payload(app, client, caplog):
    del client
    app.config["EMAIL_PROVIDER"] = "LOG"
    payload = {
        "to": ["citizen@example.com"],
        "subject": "Hello",
        "body": "World",
        "bodyType": "text",
    }

    with app.test_client() as test_client, caplog.at_level(
        "INFO", logger="api.services.notifications"
    ):
        response = test_client.post("/api/v1/notifications/email", json=payload)

    log_output = _notification_messages(caplog)
    assert response.status_code == 200
    assert '"email_address": "citizen@example.com"' in log_output
    assert '"template_id": "email-template"' in log_output
    assert '"email_subject": "Hello"' in log_output
    assert '"email_text": "World"' in log_output
