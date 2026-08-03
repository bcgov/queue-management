import importlib
import sys

import pytest


@pytest.fixture
def app(monkeypatch):
    monkeypatch.setattr(
        "flask_jwt_oidc.JwtManager.requires_auth",
        lambda self, func: func,
        raising=False,
    )
    monkeypatch.setattr(
        "flask_jwt_oidc.JwtManager.init_app",
        lambda self, app: None,
        raising=False,
    )
    monkeypatch.setenv("FLASK_CONFIGURATION", "testing")
    monkeypatch.setenv("SECRET_KEY", "test-secret")
    monkeypatch.setenv(
        "JWT_OIDC_WELL_KNOWN_CONFIG",
        "https://example.com/.well-known/openid-configuration",
    )
    monkeypatch.setenv("JWT_OIDC_JWKS_URI", "https://example.com/jwks.json")
    monkeypatch.setenv("JWT_OIDC_ISSUER", "https://example.com/")
    monkeypatch.setenv("JWT_OIDC_AUDIENCE", "theq-notifications-api")
    monkeypatch.setenv("GC_NOTIFY_API_KEY", "test-key")
    monkeypatch.setenv("GC_NOTIFY_API_BASE_URL", "https://api.notification.canada.ca/")
    monkeypatch.setenv("GC_NOTIFY_SMS_TEMPLATE_ID", "sms-template")
    monkeypatch.setenv("GC_NOTIFY_EMAIL_TEMPLATE_ID", "email-template")
    monkeypatch.setenv("APPOINTMENT_APP_URL", "http://localhost:8081")
    monkeypatch.delenv("SMS_PROVIDER", raising=False)
    monkeypatch.delenv("SMS_USE_GC_NOTIFY", raising=False)
    monkeypatch.setenv("SMS_REMINDER_TEMPLATE", "Reminder {display_name} {app_url}")
    monkeypatch.setenv(
        "SMS_CHECKIN_CONFIRMATION_TEMPLATE",
        "Checkin {ticket_number} {url}",
    )
    monkeypatch.setenv("EMAIL_PROVIDER", "GC_NOTIFY")

    for module_name in [
        "config",
        "api",
        "api.app_config",
        "api.auth.auth",
        "api.resources",
        "api.resources.notifications",
        "api.resources.email",
        "api.services.sms",
        "api.services.sms.log_notify",
        "api.services.sms.payloads",
        "api.services.email",
        "api.services.email.email_log_notify",
        "api.services.email.payloads",
        "api.services.notification_logging",
    ]:
        sys.modules.pop(module_name, None)

    from api import create_app

    app = create_app("testing")
    app.config.update(TESTING=True)
    yield app

    importlib.invalidate_caches()


@pytest.fixture
def client(app):
    return app.test_client()
