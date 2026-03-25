import importlib
import os
import sys
import uuid
from contextlib import closing

import pytest

try:
    import psycopg2
    from psycopg2 import sql
except ImportError:  # pragma: no cover - handled by session skip
    psycopg2 = None
    sql = None


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
    return importlib.import_module("manage")


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
