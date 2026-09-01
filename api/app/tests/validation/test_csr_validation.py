from __future__ import annotations

import pytest
from app.tests.api_test_support import json_of

pytestmark = [pytest.mark.validation, pytest.mark.usefixtures("seeded_database")]


def test_csr_update_rejects_an_empty_json_payload(internal_ga_client, seeded_data):
    """Assert that the CSR update endpoint returns 400 when no editable fields are provided."""
    response = internal_ga_client.put(
        f"/csrs/{seeded_data['csr_ids']['ga']}/",
        json={},
    )

    assert response.status_code == 400, response.get_data(as_text=True)
    assert json_of(response)["message"] == "No input data received for updating CSR"


def test_csr_update_rejects_editing_a_different_csr(
    internal_ga_client, seeded_data, app
):
    """Assert that a CSR cannot edit another CSR's record."""
    with app.app_context():
        from app.models.theq import CSR

        original = CSR.query.filter_by(
            csr_id=seeded_data["csr_ids"]["non_qtxn"]
        ).first()
        assert original is not None
        original_receptionist_ind = original.receptionist_ind

    response = internal_ga_client.put(
        f"/csrs/{seeded_data['csr_ids']['non_qtxn']}/",
        json={"receptionist_ind": 0},
    )

    assert response.status_code == 403, response.get_data(as_text=True)
    assert json_of(response)["message"] == "You do not have permission to edit this CSR"

    with app.app_context():
        from app.models.theq import CSR

        persisted = CSR.query.filter_by(
            csr_id=seeded_data["csr_ids"]["non_qtxn"]
        ).first()
        assert persisted is not None
        assert persisted.receptionist_ind == original_receptionist_ind


def test_csr_update_rejects_an_invalid_csr_state_type(internal_ga_client, seeded_data):
    """Assert that Marshmallow validation returns 422 when csr_state_id is not an integer."""
    response = internal_ga_client.put(
        f"/csrs/{seeded_data['csr_ids']['ga']}/",
        json={"csr_state_id": "not-an-integer"},
    )

    assert response.status_code == 422, response.get_data(as_text=True)
    assert "csr_state_id" in json_of(response)["message"]
