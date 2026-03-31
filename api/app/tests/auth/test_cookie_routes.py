import pytest
from app.tests.api_test_support import assert_unauthorized

pytestmark = [pytest.mark.auth, pytest.mark.usefixtures("seeded_database")]


def test_bare_client_receives_401_for_cookie_authenticated_login(bare_client):
    """Assert that the admin login route still rejects unauthenticated cookie requests."""
    response = bare_client.get("/login/")

    assert_unauthorized(response)


def test_internal_user_can_reach_cookie_authenticated_login(internal_ga_client):
    """Assert that an authenticated internal user still reaches the admin login redirect."""
    response = internal_ga_client.get("/login/")

    assert response.status_code == 302, response.get_data(as_text=True)
    assert response.headers["Location"].endswith("/admin/")
