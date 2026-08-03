from __future__ import annotations

import pytest
from app.tests.api_test_support import (
    assert_json_response,
    create_service_ready_citizen,
    json_of,
)

pytestmark = [pytest.mark.flows, pytest.mark.usefixtures("seeded_database")]


def _csr_state_id(app, state_name: str) -> int:
    with app.app_context():
        from app.models.theq import CSRState

        state = CSRState.query.filter_by(csr_state_name=state_name).first()
        assert state is not None
        return state.csr_state_id


def _persisted_csr_state(app, csr_id: int) -> str:
    with app.app_context():
        from app.models.theq import CSR

        csr = CSR.query.filter_by(csr_id=csr_id).first()
        assert csr is not None
        return csr.csr_state.csr_state_name


def test_csr_can_transition_from_logout_to_break(internal_ga_client, seeded_data, app):
    """Assert that a CSR can update their own state from Logout to Break."""
    break_state_id = _csr_state_id(app, "Break")

    response = internal_ga_client.put(
        f"/csrs/{seeded_data['csr_ids']['ga']}/",
        json={"csr_state_id": break_state_id},
    )

    assert_json_response(response, 200)
    assert json_of(response)["csr"]["csr_state"]["csr_state_name"] == "Break"
    assert _persisted_csr_state(app, seeded_data["csr_ids"]["ga"]) == "Break"


def test_csr_can_transition_from_break_to_back_office(
    internal_ga_client, seeded_data, app
):
    """Assert that a CSR already on Break can transition themselves into Back Office work."""
    break_state_id = _csr_state_id(app, "Break")
    back_office_state_id = _csr_state_id(app, "Back Office")
    assert_json_response(
        internal_ga_client.put(
            f"/csrs/{seeded_data['csr_ids']['ga']}/",
            json={"csr_state_id": break_state_id},
        ),
        200,
    )

    response = internal_ga_client.put(
        f"/csrs/{seeded_data['csr_ids']['ga']}/",
        json={"csr_state_id": back_office_state_id},
    )

    assert_json_response(response, 200)
    assert json_of(response)["csr"]["csr_state"]["csr_state_name"] == "Back Office"
    assert _persisted_csr_state(app, seeded_data["csr_ids"]["ga"]) == "Back Office"


def test_csr_state_update_is_rejected_while_the_csr_has_an_open_ticket(
    internal_ga_client, seeded_data, app
):
    """Assert that CSR state edits are blocked while the CSR still owns an invited or active ticket."""
    break_state_id = _csr_state_id(app, "Break")
    citizen, _service_request = create_service_ready_citizen(
        internal_ga_client,
        seeded_data,
        position=0,
        name="Open Ticket Citizen",
        service_id_key="ptax",
        channel_id_key="phone",
        quantity=1,
        counter_id_key="quick_trans",
    )
    assert_json_response(
        internal_ga_client.post(f"/citizens/{citizen['citizen_id']}/begin_service/"),
        200,
    )

    response = internal_ga_client.put(
        f"/csrs/{seeded_data['csr_ids']['ga']}/",
        json={"csr_state_id": break_state_id},
    )

    assert response.status_code == 403, response.get_data(as_text=True)
    assert (
        json_of(response)["message"] == "CSR has an open ticket and cannot be edited."
    )
    assert _persisted_csr_state(app, seeded_data["csr_ids"]["ga"]) == "Logout"
