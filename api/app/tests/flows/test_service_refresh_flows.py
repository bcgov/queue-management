import pytest
from app.tests.api_test_support import assert_json_response, json_of
from app.tests.auth.auth_support import promote_internal_csr_to_support

pytestmark = [pytest.mark.flows, pytest.mark.usefixtures("seeded_database")]


def test_ga_can_refresh_services_for_their_own_office(
    internal_ga_client, seeded_data
):
    """Assert that a GA can refresh the service lists for their own office."""
    response = internal_ga_client.get(
        f"/services/refresh/?office_id={seeded_data['office_ids']['test_office']}"
    )
    body = json_of(response)

    assert_json_response(response, 200)
    assert body["office_id"] == seeded_data["office_ids"]["test_office"]
    assert isinstance(body["quick_list"], list)
    assert isinstance(body["back_office_list"], list)


def test_ga_is_rejected_when_refreshing_a_different_office(
    internal_ga_client, seeded_data
):
    """Assert that GAs cannot refresh service lists for a different office."""
    response = internal_ga_client.get(
        f"/services/refresh/?office_id={seeded_data['office_ids']['limited_office']}"
    )

    assert response.status_code == 403, response.get_data(as_text=True)
    assert "cannot refresh" in response.get_data(as_text=True)


def test_support_user_can_refresh_services_for_any_office(
    app, internal_nonqtxn_client, seeded_data
):
    """Assert that SUPPORT users can refresh service lists outside their home office."""
    promote_internal_csr_to_support(app)

    response = internal_nonqtxn_client.get(
        f"/services/refresh/?office_id={seeded_data['office_ids']['limited_office']}"
    )
    body = json_of(response)

    assert_json_response(response, 200)
    assert body["office_id"] == seeded_data["office_ids"]["limited_office"]
