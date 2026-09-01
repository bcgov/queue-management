import pytest
from app.tests.api_test_support import assert_json_response
from app.tests.contracts.conftest import validate_schema

pytestmark = [pytest.mark.contracts, pytest.mark.smoke]


def test_assert_json_response_accepts_application_json(minimal_app):
    """Assert that JSON responses with the expected status pass the shared helper."""
    response = minimal_app.response_class(
        response='{"message":"ok"}',
        status=200,
        mimetype="application/json",
    )

    assert_json_response(response, 200)


def test_assert_json_response_rejects_non_json_content_type(minimal_app):
    """Assert that the shared JSON helper rejects non-JSON content types."""
    response = minimal_app.response_class(response="ok", status=200, mimetype="text/html")

    with pytest.raises(AssertionError):
        assert_json_response(response, 200)


def test_validate_schema_reports_the_failing_path():
    """Assert that schema validation failures include the nested field path."""
    with pytest.raises(pytest.fail.Exception, match=r"items\.0\.name"):
        validate_schema(
            {"items": [{}]},
            {
                "type": "object",
                "required": ["items"],
                "properties": {
                    "items": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "required": ["name"],
                            "properties": {"name": {"type": "string"}},
                        },
                    }
                },
            },
        )
