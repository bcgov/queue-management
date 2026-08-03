import pytest
from app.tests.api_test_support import assert_json_response, json_of

pytestmark = [pytest.mark.validation, pytest.mark.usefixtures("seeded_database")]


def test_service_refresh_requires_an_office_id(internal_ga_client):
    """Assert that refresh requests without office_id fail with the stable error payload."""
    response = internal_ga_client.get("/services/refresh/")

    assert_json_response(response, 400)
    assert json_of(response)["message"] == "no office specified"


def test_service_refresh_rejects_non_integer_office_ids(internal_ga_client):
    """Assert that refresh requests reject non-numeric office ids with a stable validation message."""
    response = internal_ga_client.get("/services/refresh/?office_id=abc")

    assert_json_response(response, 400)
    assert json_of(response)["message"] == "office_id must be an integer."
