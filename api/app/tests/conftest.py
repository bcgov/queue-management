import copy
import importlib
import os
import sys
import uuid
from contextlib import closing

import pytest

from app.tests.api_test_support import ApiClient

try:
    import psycopg2
    from psycopg2 import sql
except ImportError:  # pragma: no cover - handled by session skip
    psycopg2 = None
    sql = None


TEST_IDENTITIES = {
    "internal_ga": {
        "username": "cfms-postman-operator",
        "identity_provider": "idir",
        "realm_access": {"roles": ["internal_user"]},
        "email": "ga@example.com",
        "display_name": "GA User",
        "family_name": "GA",
    },
    "internal_nonqtxn": {
        "username": "cfms-postman-non-operator",
        "identity_provider": "idir",
        "realm_access": {"roles": ["internal_user"]},
        "email": "csr@example.com",
        "display_name": "CSR User",
        "family_name": "CSR",
    },
    "public_user": {
        "username": "theq-public-user",
        "identity_provider": "bceid",
        "realm_access": {"roles": ["online_appointment_user"]},
        "email": "public@example.com",
        "display_name": "Public User",
        "family_name": "Public",
    },
    "public_user_alt": {
        "username": "theq-public-user-alt",
        "identity_provider": "bceid",
        "realm_access": {"roles": ["online_appointment_user"]},
        "email": "public-alt@example.com",
        "display_name": "Public Alt User",
        "family_name": "PublicAlt",
    },
}


def _db_settings():
    return {
        "engine": os.getenv("TEST_DATABASE_ENGINE", "postgresql+psycopg2"),
        "host": os.getenv("TEST_DATABASE_HOST", os.getenv("DATABASE_HOST", "127.0.0.1")),
        "port": os.getenv("TEST_DATABASE_PORT", os.getenv("DATABASE_PORT", "5432")),
        "user": os.getenv("TEST_DATABASE_USERNAME", os.getenv("DATABASE_USERNAME", "postgres")),
        "password": os.getenv("TEST_DATABASE_PASSWORD", os.getenv("DATABASE_PASSWORD", "root")),
        "admin_db": os.getenv("TEST_DATABASE_ADMIN_DB", "postgres"),
    }


def _connect(database_name):
    settings = _db_settings()
    return psycopg2.connect(
        dbname=database_name,
        user=settings["user"],
        password=settings["password"],
        host=settings["host"],
        port=settings["port"],
    )


def _patch_jwt_manager():
    from flask_jwt_oidc import JwtManager

    if getattr(JwtManager, "_theq_pytest_patched", False):
        return

    def passthrough(self, *decorator_args, **decorator_kwargs):
        del self, decorator_kwargs
        if decorator_args and callable(decorator_args[0]) and len(decorator_args) == 1:
            return decorator_args[0]

        def decorator(func):
            return func

        return decorator

    def init_app(self, app):
        app.extensions["theq_test_jwt"] = self

    JwtManager.has_one_of_roles = passthrough
    JwtManager.requires_auth = passthrough
    JwtManager.requires_auth_cookie = passthrough
    JwtManager.init_app = init_app
    JwtManager._theq_pytest_patched = True


def _install_identity_loader(app):
    if app.config.get("THEQ_TEST_IDENTITY_LOADER"):
        return

    from flask import g, request

    app.config["TEST_IDENTITIES"] = TEST_IDENTITIES
    app.config["DISABLE_AUTO_REFRESH"] = True

    @app.before_request
    def _load_theq_test_identity():
        identity_name = request.headers.get("X-TheQ-Test-Identity")
        identity = app.config["TEST_IDENTITIES"].get(identity_name)
        if identity:
            g.jwt_oidc_token_info = copy.deepcopy(identity)

    app.config["THEQ_TEST_IDENTITY_LOADER"] = True


def _stub_integrations():
    import qsystem
    from app.utilities.snowplow import SnowPlow

    qsystem.socketio.emit = lambda *args, **kwargs: None

    for method_name in (
        "add_citizen",
        "choose_service",
        "snowplow_event",
        "snowplow_appointment",
    ):
        setattr(SnowPlow, method_name, staticmethod(lambda *args, **kwargs: None))

    email_stub = lambda *args, **kwargs: None
    email_contents_stub = lambda *args, **kwargs: ("test@example.com", "Subject", "Body")
    sms_stub = lambda *args, **kwargs: True

    patch_targets = {
        "app.resources.theq.citizen.citizen_add_to_queue": {
            "send_email": email_stub,
            "get_walkin_spot_confirmation_email_contents": email_contents_stub,
            "send_walkin_spot_confirmation_sms": sms_stub,
        },
        "app.resources.theq.citizen.citizen_detail": {
            "send_email": email_stub,
            "get_walkin_reminder_email_contents": email_contents_stub,
            "send_walkin_reminder_sms": sms_stub,
        },
        "app.resources.theq.user.user": {
            "send_sms": sms_stub,
        },
        "app.resources.bookings.appointment.appointment_post": {
            "send_email": email_stub,
            "get_confirmation_email_contents": email_contents_stub,
            "get_blackout_email_contents": email_contents_stub,
            "send_sms": sms_stub,
        },
        "app.resources.bookings.appointment.appointment_put": {
            "send_email": email_stub,
            "get_confirmation_email_contents": email_contents_stub,
            "send_sms": sms_stub,
        },
        "app.resources.bookings.appointment.appointment_delete": {
            "send_email": email_stub,
            "get_cancel_email_contents": email_contents_stub,
        },
    }

    for module_name, attributes in patch_targets.items():
        module = importlib.import_module(module_name)
        for attribute_name, value in attributes.items():
            setattr(module, attribute_name, value)


@pytest.fixture(scope="session")
def postgres_database():
    if psycopg2 is None:
        pytest.skip("psycopg2 is required for the SQLAlchemy smoke suite")

    database_name = f"qsystem_sqlalchemy_smoke_{uuid.uuid4().hex[:12]}"
    settings = _db_settings()

    try:
        with closing(_connect(settings["admin_db"])) as connection:
            connection.autocommit = True
            with connection.cursor() as cursor:
                cursor.execute(
                    sql.SQL("CREATE DATABASE {}").format(sql.Identifier(database_name))
                )
    except Exception as exc:  # pragma: no cover - depends on local services
        pytest.skip(f"unable to create disposable Postgres database: {exc}")

    original_env = {
        key: os.environ.get(key)
        for key in (
            "FLASK_CONFIGURATION",
            "DATABASE_ENGINE",
            "DATABASE_HOST",
            "DATABASE_PORT",
            "DATABASE_USERNAME",
            "DATABASE_PASSWORD",
            "DATABASE_NAME",
            "JWT_OIDC_WELL_KNOWN_CONFIG",
            "JWT_OIDC_JWKS_URI",
            "JWT_OIDC_ISSUER",
            "JWT_OIDC_AUDIENCE",
        )
    }

    os.environ.update(
        {
            "FLASK_CONFIGURATION": "localhost",
            "DATABASE_ENGINE": settings["engine"],
            "DATABASE_HOST": settings["host"],
            "DATABASE_PORT": settings["port"],
            "DATABASE_USERNAME": settings["user"],
            "DATABASE_PASSWORD": settings["password"],
            "DATABASE_NAME": database_name,
            "JWT_OIDC_WELL_KNOWN_CONFIG": "",
            "JWT_OIDC_JWKS_URI": "https://example.com/jwks.json",
            "JWT_OIDC_ISSUER": "https://example.com/",
            "JWT_OIDC_AUDIENCE": "queue-api-tests",
        }
    )

    try:
        yield {
            "database_name": database_name,
            "database_uri": (
                f"{settings['engine']}://{settings['user']}:{settings['password']}"
                f"@{settings['host']}:{settings['port']}/{database_name}"
            ),
        }
    finally:
        for module_name in ("manage", "qsystem"):
            module = sys.modules.get(module_name)
            if module is not None and hasattr(module, "db"):
                try:
                    module.db.session.remove()
                    if hasattr(module, "application"):
                        with module.application.app_context():
                            module.db.engine.dispose()
                except Exception:
                    pass

        for module_name in list(sys.modules):
            if module_name == "app" or module_name.startswith("app.") or module_name in ("manage", "qsystem"):
                sys.modules.pop(module_name, None)

        try:
            with closing(_connect(settings["admin_db"])) as connection:
                connection.autocommit = True
                with connection.cursor() as cursor:
                    cursor.execute(
                        sql.SQL(
                            "SELECT pg_terminate_backend(pid) "
                            "FROM pg_stat_activity WHERE datname = %s AND pid <> pg_backend_pid()"
                        ),
                        (database_name,),
                    )
                    cursor.execute(
                        sql.SQL("DROP DATABASE IF EXISTS {}").format(sql.Identifier(database_name))
                    )
        finally:
            for key, value in original_env.items():
                if value is None:
                    os.environ.pop(key, None)
                else:
                    os.environ[key] = value


@pytest.fixture(scope="session")
def app_module(postgres_database):
    del postgres_database
    _patch_jwt_manager()
    module = importlib.import_module("manage")
    _install_identity_loader(module.application)
    _stub_integrations()
    return module


@pytest.fixture(scope="session")
def app(app_module):
    return app_module.application


@pytest.fixture(scope="session")
def db(app_module):
    return app_module.db


@pytest.fixture(scope="session")
def cli_runner(app):
    return app.test_cli_runner()


@pytest.fixture(scope="session")
def client(app):
    return app.test_client()


@pytest.fixture(scope="session")
def migrated_database(cli_runner):
    result = cli_runner.invoke(args=["db", "upgrade"])
    assert result.exit_code == 0, result.output
    return result


@pytest.fixture()
def seeded_database(cli_runner, migrated_database, app):
    del migrated_database

    with app.app_context():
        from qsystem import db

        db.session.remove()

    result = cli_runner.invoke(args=["bootstrap"])
    assert result.exit_code == 0, result.output

    with app.app_context():
        from qsystem import cache, db

        db.session.remove()
        cache.clear()

    return result


@pytest.fixture()
def seeded_data(seeded_database, app):
    del seeded_database

    with app.app_context():
        from app.models.bookings import ExamType, Invigilator, Room
        from app.models.theq import CSR, Channel, Counter, Office, Service

        office_test = Office.query.filter_by(office_name="Test Office").first()
        office_limited = Office.query.filter_by(office_name="100 Mile House").first()
        quick_trans = Counter.query.filter_by(counter_name="Quick Trans").first()
        counter = Counter.query.filter_by(counter_name="Counter").first()
        phone_channel = Channel.query.filter_by(channel_name="Phone").first()
        email_channel = Channel.query.filter_by(channel_name="Email/Fax/Mail").first()
        msp_service = Service.query.filter_by(service_name="Payment - MSP").first()
        ptax_service = Service.query.filter_by(service_name="Other - PTAX").first()
        limited_office_service = Service.query.filter_by(service_name="Deferment Application").first()
        room = Room.query.filter_by(room_name="Boardroom 1").first()
        invigilators = Invigilator.query.filter_by(office_id=office_test.office_id).order_by(Invigilator.invigilator_id).all()
        exam_type = ExamType.query.order_by(ExamType.exam_type_id).first()
        ga = CSR.query.filter_by(username="cfms-postman-operator").first()
        non_qtxn = CSR.query.filter_by(username="cfms-postman-non-operator").first()

        return {
            "office_ids": {
                "test_office": office_test.office_id,
                "limited_office": office_limited.office_id,
            },
            "office_timezones": {
                "test_office": office_test.timezone.timezone_name,
                "limited_office": office_limited.timezone.timezone_name,
            },
            "counter_ids": {
                "quick_trans": quick_trans.counter_id,
                "counter": counter.counter_id,
            },
            "channel_ids": {
                "phone": phone_channel.channel_id,
                "email": email_channel.channel_id,
            },
            "service_ids": {
                "msp": msp_service.service_id,
                "ptax": ptax_service.service_id,
                "limited_office_service": limited_office_service.service_id,
            },
            "csr_ids": {
                "ga": ga.csr_id,
                "non_qtxn": non_qtxn.csr_id,
            },
            "room_id": room.room_id,
            "invigilator_ids": [invigilator.invigilator_id for invigilator in invigilators],
            "exam_type_id": exam_type.exam_type_id,
        }


@pytest.fixture()
def api_client_factory(app):
    def factory(identity_name):
        return ApiClient(app.test_client(), identity_name)

    return factory


@pytest.fixture()
def internal_ga_client(api_client_factory):
    return api_client_factory("internal_ga")


@pytest.fixture()
def internal_nonqtxn_client(api_client_factory):
    return api_client_factory("internal_nonqtxn")


@pytest.fixture()
def public_client(api_client_factory):
    return api_client_factory("public_user")


@pytest.fixture()
def public_client_alt(api_client_factory):
    return api_client_factory("public_user_alt")
