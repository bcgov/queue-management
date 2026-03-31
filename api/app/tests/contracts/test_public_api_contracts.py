import pytest
from app.tests.api_test_support import assert_json_response, json_of
from app.tests.contracts.conftest import validate_schema
from app.tests.contracts.schemas import PUBLIC_USER_LIST_SCHEMA

pytestmark = [pytest.mark.contracts, pytest.mark.usefixtures("seeded_database")]


def test_public_user_create_response_matches_the_contract(public_client):
    """Assert that public-user creation returns the stable user profile contract."""
    response = public_client.post("/users/")
    body = json_of(response)

    assert_json_response(response, 200)
    validate_schema(body, PUBLIC_USER_LIST_SCHEMA)
    assert body[0]["username"].endswith("@bceid")


def test_public_user_me_response_matches_the_contract(public_client):
    """Assert that the public-user self endpoint preserves the stable user profile contract."""
    create_response = public_client.post("/users/")
    assert_json_response(create_response, 200)

    response = public_client.get("/users/me/")
    body = json_of(response)

    assert_json_response(response, 200)
    validate_schema(body, PUBLIC_USER_LIST_SCHEMA)
