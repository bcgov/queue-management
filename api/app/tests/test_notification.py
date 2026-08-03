import pytest
from app.utilities.notification_email import send_email
from flask import Flask

pytestmark = pytest.mark.smoke


def test_send_email_posts_json_payload_with_timeout(monkeypatch):
    """Assert that notification emails are sent as JSON with the expected auth header and timeout."""
    app = Flask(__name__)
    app.config["NOTIFICATIONS_EMAIL_ENDPOINT"] = "https://example.com/email"

    recorded = {}

    class Response:
        def raise_for_status(self):
            return None

    def fake_post(url, headers=None, json=None, timeout=None):
        recorded["url"] = url
        recorded["headers"] = headers
        recorded["json"] = json
        recorded["timeout"] = timeout
        return Response()

    monkeypatch.setattr("app.utilities.notification_email.requests.post", fake_post)

    with app.app_context():
        send_email(
            "token-123",
            "Subject",
            "citizen@example.com",
            "noreply@example.com",
            "<p>Hello</p>",
        )

    assert recorded["url"] == "https://example.com/email"
    assert recorded["headers"]["Authorization"] == "Bearer token-123"
    assert recorded["json"]["subject"] == "Subject"
    assert recorded["timeout"] == 30
