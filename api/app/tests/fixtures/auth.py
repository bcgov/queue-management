import pytest
from app.tests.api_test_support import ApiClient


@pytest.fixture()
def api_client_factory(app):
    def factory(identity_name=None, token="theq-test-token"):
        return ApiClient(app.test_client(), identity_name, token)

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


@pytest.fixture()
def public_client_malformed(api_client_factory):
    return api_client_factory("public_user_malformed")


@pytest.fixture()
def public_client_missing_username(api_client_factory):
    return api_client_factory("public_user_missing_username")


@pytest.fixture()
def reminder_job_client(api_client_factory):
    return api_client_factory("reminder_job")


@pytest.fixture()
def bare_client(api_client_factory):
    return api_client_factory(identity_name=None, token=None)
