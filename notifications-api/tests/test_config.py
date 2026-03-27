import importlib


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
    monkeypatch.setenv("JWT_OIDC_AUDIENCE", "theq-notifications-api")

    import api
    import api.app_config as config

    importlib.reload(config)
    importlib.reload(api)

    app = api.create_app()

    assert app.config["TESTING"] is True


def test_sms_provider_uses_app_config(app):
    from api.services.sms import get_sms_service
    from api.services.sms.gc_notify import GCNotify

    with app.app_context():
        app.config["SMS_USE_GC_NOTIFY"] = True
        assert isinstance(get_sms_service(), GCNotify)


def test_email_provider_uses_app_config(app):
    from api.services.email import get_email_service
    from api.services.email.email_ches_notify import EmailChesNotify

    with app.app_context():
        app.config["EMAIL_PROVIDER"] = "CHES"
        assert isinstance(get_email_service(), EmailChesNotify)
