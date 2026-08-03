import importlib
from urllib.error import URLError

import pytest


def test_create_app_prefers_flask_configuration(monkeypatch):
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
    monkeypatch.setenv("FLASK_ENV", "production")
    monkeypatch.setenv("SECRET_KEY", "test-secret")
    monkeypatch.setenv(
        "JWT_OIDC_WELL_KNOWN_CONFIG",
        "https://example.com/.well-known/openid-configuration",
    )
    monkeypatch.setenv("JWT_OIDC_JWKS_URI", "https://example.com/jwks.json")
    monkeypatch.setenv("JWT_OIDC_ISSUER", "https://example.com/")
    monkeypatch.setenv("JWT_OIDC_AUDIENCE", "theq-notifications-api")

    import api
    import api.app_config as config

    importlib.reload(config)
    importlib.reload(api)

    app = api.create_app()

    assert app.config["TESTING"] is True


def test_create_app_falls_back_to_direct_jwks_when_well_known_unreachable(monkeypatch):
    calls = []

    monkeypatch.setattr(
        "flask_jwt_oidc.JwtManager.requires_auth",
        lambda self, func: func,
        raising=False,
    )

    def fake_init_app(self, app):
        calls.append(app.config.get("JWT_OIDC_WELL_KNOWN_CONFIG"))
        if len(calls) == 1:
            raise URLError("connection refused")

    monkeypatch.setattr(
        "flask_jwt_oidc.JwtManager.init_app",
        fake_init_app,
        raising=False,
    )
    monkeypatch.setenv("FLASK_CONFIGURATION", "testing")
    monkeypatch.setenv("SECRET_KEY", "test-secret")
    monkeypatch.setenv(
        "JWT_OIDC_WELL_KNOWN_CONFIG",
        "http://localhost:8085/auth/realms/servicebc-local/.well-known/openid-configuration",
    )
    monkeypatch.setenv(
        "JWT_OIDC_JWKS_URI",
        "http://keycloak:8080/auth/realms/servicebc-local/protocol/openid-connect/certs",
    )
    monkeypatch.setenv(
        "JWT_OIDC_ISSUER",
        "http://localhost:8085/auth/realms/servicebc-local",
    )
    monkeypatch.setenv("JWT_OIDC_AUDIENCE", "theq-notifications-api")

    import api
    import api.app_config as config

    importlib.reload(config)
    importlib.reload(api)

    app = api.create_app()

    assert app.config["JWT_OIDC_WELL_KNOWN_CONFIG"] == (
        "http://localhost:8085/auth/realms/servicebc-local/.well-known/openid-configuration"
    )
    assert calls == [
        "http://localhost:8085/auth/realms/servicebc-local/.well-known/openid-configuration",
        None,
    ]


def test_create_app_raises_when_well_known_unreachable_without_fallback(monkeypatch):
    monkeypatch.setattr(
        "flask_jwt_oidc.JwtManager.requires_auth",
        lambda self, func: func,
        raising=False,
    )
    monkeypatch.setattr(
        "flask_jwt_oidc.JwtManager.init_app",
        lambda self, app: (_ for _ in ()).throw(URLError("connection refused")),
        raising=False,
    )
    monkeypatch.setenv("FLASK_CONFIGURATION", "testing")
    monkeypatch.setenv("SECRET_KEY", "test-secret")
    monkeypatch.setenv(
        "JWT_OIDC_WELL_KNOWN_CONFIG",
        "http://localhost:8085/auth/realms/servicebc-local/.well-known/openid-configuration",
    )
    monkeypatch.delenv("JWT_OIDC_JWKS_URI", raising=False)
    monkeypatch.delenv("JWT_OIDC_ISSUER", raising=False)
    monkeypatch.setenv("JWT_OIDC_AUDIENCE", "theq-notifications-api")

    import api
    import api.app_config as config

    importlib.reload(config)
    importlib.reload(api)

    with pytest.raises(URLError):
        api.create_app()


def test_sms_provider_uses_app_config(app):
    from api.services.sms import get_sms_service
    from api.services.sms.custom_notify import CustomNotify
    from api.services.sms.gc_notify import GCNotify
    from api.services.sms.log_notify import SmsLogNotify

    with app.app_context():
        app.config.pop("SMS_PROVIDER", None)
        assert isinstance(get_sms_service(), CustomNotify)
        assert app.config["SMS_USE_GC_NOTIFY"] is False

        app.config["SMS_PROVIDER"] = "GC_NOTIFY"
        assert isinstance(get_sms_service(), GCNotify)
        assert app.config["SMS_USE_GC_NOTIFY"] is True

        app.config["SMS_PROVIDER"] = "LOG"
        assert isinstance(get_sms_service(), SmsLogNotify)
        assert app.config["SMS_USE_GC_NOTIFY"] is False

        app.config["SMS_PROVIDER"] = "CUSTOM"
        assert isinstance(get_sms_service(), CustomNotify)
        assert app.config["SMS_USE_GC_NOTIFY"] is False


def test_email_provider_uses_app_config(app):
    from api.services.email import get_email_service
    from api.services.email.email_ches_notify import EmailChesNotify
    from api.services.email.email_gc_notify import EmailGCNotify
    from api.services.email.email_log_notify import EmailLogNotify

    with app.app_context():
        app.config["EMAIL_PROVIDER"] = "GC_NOTIFY"
        assert isinstance(get_email_service(), EmailGCNotify)

        app.config["EMAIL_PROVIDER"] = "CHES"
        assert isinstance(get_email_service(), EmailChesNotify)

        app.config["EMAIL_PROVIDER"] = "LOG"
        assert isinstance(get_email_service(), EmailLogNotify)
