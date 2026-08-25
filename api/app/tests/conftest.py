from pathlib import Path

import pytest

pytest_plugins = [
    "app.tests.fixtures.auth",
    "app.tests.fixtures.db",
    "app.tests.fixtures.smoke",
]

CONTRACT_SMOKE_FILES = {
    "test_contract_helpers.py",
    "test_contract_strictness.py",
}
DB_BACKED_TOP_LEVEL_FILES = {
    "test_flask3_admin.py",
    "test_schema_compatibility.py",
    "test_sqlalchemy.py",
}


def pytest_addoption(parser):
    parser.addoption(
        "--require-integration-db",
        action="store_true",
        default=False,
        help="Fail fast when the integration database is unavailable.",
    )


def _is_integration_path(path: Path) -> bool:
    path_str = path.as_posix()

    if "/app/tests/auth/" in path_str:
        return True
    if "/app/tests/flows/" in path_str:
        return True
    if "/app/tests/validation/" in path_str:
        return True
    if "/app/tests/contracts/" in path_str and path.name not in CONTRACT_SMOKE_FILES:
        return True
    if path.name in DB_BACKED_TOP_LEVEL_FILES:
        return True
    return False


def pytest_collection_modifyitems(config, items):
    del config

    for item in items:
        path = Path(str(item.fspath))
        if _is_integration_path(path) and not item.get_closest_marker("integration"):
            item.add_marker(pytest.mark.integration)
