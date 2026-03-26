from datetime import datetime

from flask import Flask

from app.utilities.date_util import add_delta_to_time, current_pacific_time
from app.utilities.notification_email import send_email
from app.utilities.timezone_utils import as_utc, get_timezone, localize


def test_localize_preserves_dst_offset_for_vancouver():
    localized = localize(datetime(2026, 3, 8, 1, 30), "America/Vancouver")

    assert localized.tzinfo == get_timezone("America/Vancouver")
    assert localized.utcoffset().total_seconds() == -8 * 3600


def test_as_utc_marks_naive_datetimes_as_utc():
    converted = as_utc(datetime(2026, 3, 8, 9, 30))

    assert converted.utcoffset().total_seconds() == 0
    assert converted.isoformat() == "2026-03-08T09:30:00+00:00"


def test_add_delta_to_time_returns_zoneinfo_backed_time():
    shifted = add_delta_to_time(datetime.strptime("08:30", "%H:%M").time(), "America/Vancouver", minutes=30)

    assert shifted.strftime("%H:%M") == "09:00"
    assert shifted.tzinfo == get_timezone("America/Vancouver")


def test_current_pacific_time_uses_vancouver_zone():
    pacific_now = current_pacific_time()

    assert pacific_now.tzinfo == get_timezone("America/Vancouver")


def test_send_email_posts_json_payload_with_timeout(monkeypatch):
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
        send_email("token-123", "Subject", "citizen@example.com", "noreply@example.com", "<p>Hello</p>")

    assert recorded["url"] == "https://example.com/email"
    assert recorded["headers"]["Authorization"] == "Bearer token-123"
    assert recorded["json"]["subject"] == "Subject"
    assert recorded["timeout"] == 30
