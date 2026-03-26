from __future__ import annotations

from typing import Optional

import pytest

from app.tests.api_test_support import assert_status, json_of


pytestmark = [pytest.mark.flows, pytest.mark.usefixtures("seeded_database")]


def _create_citizen(api_client, position: int, *, name: str, comments: Optional[str] = None):
    payload = {"citizen_name": name}
    if comments is not None:
        payload["citizen_comments"] = comments

    response = api_client.post(
        f"/citizens/{position}/add_citizen/",
        json=payload,
    )
    assert_status(response, 201)
    return json_of(response)["citizen"]


def _update_citizen(api_client, citizen_id: int, **payload):
    response = api_client.put(f"/citizens/{citizen_id}/", json=payload)
    assert_status(response, 200)
    return json_of(response)["citizen"]


def _create_service_request(api_client, citizen_id: int, *, service_id: int, channel_id: int, quantity: int):
    response = api_client.post(
        "/service_requests/",
        json={
            "service_request": {
                "citizen_id": citizen_id,
                "service_id": service_id,
                "channel_id": channel_id,
                "quantity": quantity,
            }
        },
    )
    assert_status(response, 201)
    return json_of(response)["service_request"]


def _citizen_detail(api_client, citizen_id: int):
    response = api_client.get(f"/citizens/{citizen_id}/")
    assert_status(response, 200)
    return json_of(response)["citizen"]


def _queue_ids(api_client) -> list[int]:
    response = api_client.get("/citizens/")
    assert_status(response, 200)
    return [citizen["citizen_id"] for citizen in json_of(response)["citizens"]]


def test_qt1_specific_invite_additional_service_and_reactivate(internal_ga_client, seeded_data, app):
    citizen = _create_citizen(internal_ga_client, 0, name="QT1 Citizen", comments="Needs property tax")
    updated = _update_citizen(
        internal_ga_client,
        citizen["citizen_id"],
        citizen_name="QT1 Citizen",
        citizen_comments="Needs property tax",
        qt_xn_citizen_ind=0,
        counter_id=seeded_data["counter_ids"]["counter"],
    )

    first_service = _create_service_request(
        internal_ga_client,
        updated["citizen_id"],
        service_id=seeded_data["service_ids"]["ptax"],
        channel_id=seeded_data["channel_ids"]["phone"],
        quantity=3,
    )
    assert first_service["quantity"] == 3

    add_to_queue_response = internal_ga_client.post(f"/citizens/{updated['citizen_id']}/add_to_queue/")
    specific_invite_response = internal_ga_client.post(f"/citizens/{updated['citizen_id']}/invite/")
    begin_service_response = internal_ga_client.post(f"/citizens/{updated['citizen_id']}/begin_service/")

    assert_status(add_to_queue_response, 200)
    assert_status(specific_invite_response, 200)
    assert_status(begin_service_response, 200)

    second_service = _create_service_request(
        internal_ga_client,
        updated["citizen_id"],
        service_id=seeded_data["service_ids"]["msp"],
        channel_id=seeded_data["channel_ids"]["email"],
        quantity=1,
    )
    reactivate_response = internal_ga_client.post(f"/service_requests/{first_service['sr_id']}/activate/")
    finish_response = internal_ga_client.post(f"/citizens/{updated['citizen_id']}/finish_service/")

    assert second_service["service_id"] == seeded_data["service_ids"]["msp"]
    assert_status(reactivate_response, 200)
    assert_status(finish_response, 200)
    assert _queue_ids(internal_ga_client) == []

    with app.app_context():
        from app.models.theq import Citizen, ServiceReq

        citizen_model = Citizen.query.filter_by(citizen_id=updated["citizen_id"]).first()
        sr_models = ServiceReq.query.filter_by(citizen_id=updated["citizen_id"]).order_by(ServiceReq.sr_number).all()
        assert citizen_model.cs.cs_state_name == "Received Services"
        assert [service_request.sr_state.sr_code for service_request in sr_models] == ["Complete", "Complete"]


def test_qt2_begin_hold_resume_finish_flow(internal_ga_client, seeded_data):
    citizen = _create_citizen(internal_ga_client, 0, name="QT2 Citizen")
    _update_citizen(
        internal_ga_client,
        citizen["citizen_id"],
        citizen_name="QT2 Citizen",
        counter_id=seeded_data["counter_ids"]["counter"],
    )
    _create_service_request(
        internal_ga_client,
        citizen["citizen_id"],
        service_id=seeded_data["service_ids"]["ptax"],
        channel_id=seeded_data["channel_ids"]["phone"],
        quantity=2,
    )

    assert_status(internal_ga_client.post(f"/citizens/{citizen['citizen_id']}/begin_service/"), 200)
    hold_response = internal_ga_client.post(f"/citizens/{citizen['citizen_id']}/place_on_hold/")
    service_requests_response = internal_ga_client.get(f"/citizens/{citizen['citizen_id']}/service_requests/")
    resume_response = internal_ga_client.post(f"/citizens/{citizen['citizen_id']}/begin_service/")
    finish_response = internal_ga_client.post(f"/citizens/{citizen['citizen_id']}/finish_service/")

    assert_status(hold_response, 200)
    assert_status(service_requests_response, 200)
    assert_status(resume_response, 200)
    assert_status(finish_response, 200)
    assert _queue_ids(internal_ga_client) == []


def test_qt3_citizen_leaves_after_create(internal_ga_client, app):
    citizen = _create_citizen(internal_ga_client, 0, name="QT3 Citizen")
    leave_response = internal_ga_client.post(f"/citizens/{citizen['citizen_id']}/citizen_left/")

    assert_status(leave_response, 200)

    with app.app_context():
        from app.models.theq import Citizen

        citizen_model = Citizen.query.filter_by(citizen_id=citizen["citizen_id"]).first()
        assert citizen_model.cs.cs_state_name == "Left before receiving services"


def test_qt4_citizen_leaves_after_waiting(internal_ga_client, seeded_data, app):
    citizen = _create_citizen(internal_ga_client, 0, name="QT4 Citizen")
    _create_service_request(
        internal_ga_client,
        citizen["citizen_id"],
        service_id=seeded_data["service_ids"]["ptax"],
        channel_id=seeded_data["channel_ids"]["phone"],
        quantity=1,
    )
    assert_status(internal_ga_client.post(f"/citizens/{citizen['citizen_id']}/add_to_queue/"), 200)
    leave_response = internal_ga_client.post(f"/citizens/{citizen['citizen_id']}/citizen_left/")

    assert_status(leave_response, 200)

    with app.app_context():
        from app.models.theq import Citizen

        citizen_model = Citizen.query.filter_by(citizen_id=citizen["citizen_id"]).first()
        assert citizen_model.cs.cs_state_name == "Left before receiving services"


def test_qt5_update_service_request_quantity_and_service(internal_ga_client, seeded_data, app):
    citizen = _create_citizen(internal_ga_client, 0, name="QT5 Citizen")
    service_request = _create_service_request(
        internal_ga_client,
        citizen["citizen_id"],
        service_id=seeded_data["service_ids"]["ptax"],
        channel_id=seeded_data["channel_ids"]["phone"],
        quantity=3,
    )
    assert_status(internal_ga_client.post(f"/citizens/{citizen['citizen_id']}/begin_service/"), 200)

    quantity_update = internal_ga_client.put(
        f"/service_requests/{service_request['sr_id']}/",
        json={"quantity": 5},
    )
    service_update = internal_ga_client.put(
        f"/service_requests/{service_request['sr_id']}/",
        json={"service_id": seeded_data["service_ids"]["msp"]},
    )
    finish_response = internal_ga_client.post(f"/citizens/{citizen['citizen_id']}/finish_service/")

    assert_status(quantity_update, 200)
    assert_status(service_update, 200)
    assert_status(finish_response, 200)

    with app.app_context():
        from app.models.theq import ServiceReq

        service_request_model = ServiceReq.query.filter_by(sr_id=service_request["sr_id"]).first()
        assert service_request_model.quantity == 5
        assert service_request_model.service_id == seeded_data["service_ids"]["msp"]


def test_qt6_generic_invite_prefers_quick_trans_counter(internal_ga_client, seeded_data):
    first_citizen = _create_citizen(internal_ga_client, 0, name="QT6 First")
    _update_citizen(
        internal_ga_client,
        first_citizen["citizen_id"],
        citizen_name="QT6 First",
        qt_xn_citizen_ind=0,
        counter_id=seeded_data["counter_ids"]["counter"],
    )
    _create_service_request(
        internal_ga_client,
        first_citizen["citizen_id"],
        service_id=seeded_data["service_ids"]["ptax"],
        channel_id=seeded_data["channel_ids"]["phone"],
        quantity=1,
    )
    assert_status(internal_ga_client.post(f"/citizens/{first_citizen['citizen_id']}/add_to_queue/"), 200)

    second_citizen = _create_citizen(internal_ga_client, 1, name="QT6 Second")
    _update_citizen(
        internal_ga_client,
        second_citizen["citizen_id"],
        citizen_name="QT6 Second",
        qt_xn_citizen_ind=1,
        counter_id=seeded_data["counter_ids"]["quick_trans"],
    )
    _create_service_request(
        internal_ga_client,
        second_citizen["citizen_id"],
        service_id=seeded_data["service_ids"]["msp"],
        channel_id=seeded_data["channel_ids"]["email"],
        quantity=1,
    )
    assert_status(internal_ga_client.post(f"/citizens/{second_citizen['citizen_id']}/add_to_queue/"), 200)

    first_invite = internal_ga_client.post("/citizens/invite/", json={})
    assert_status(first_invite, 200)
    assert json_of(first_invite)["citizen"]["citizen_id"] == second_citizen["citizen_id"]
    assert_status(internal_ga_client.post(f"/citizens/{second_citizen['citizen_id']}/begin_service/"), 200)
    assert_status(internal_ga_client.post(f"/citizens/{second_citizen['citizen_id']}/finish_service/"), 200)

    second_invite = internal_ga_client.post("/citizens/invite/", json={})
    assert_status(second_invite, 200)
    assert json_of(second_invite)["citizen"]["citizen_id"] == first_citizen["citizen_id"]
    assert_status(internal_ga_client.post(f"/citizens/{first_citizen['citizen_id']}/citizen_left/"), 200)
    assert _queue_ids(internal_ga_client) == []


def test_qt7_generic_invite_prefers_standard_counter(internal_nonqtxn_client, seeded_data):
    first_citizen = _create_citizen(internal_nonqtxn_client, 0, name="QT7 First")
    _update_citizen(
        internal_nonqtxn_client,
        first_citizen["citizen_id"],
        citizen_name="QT7 First",
        qt_xn_citizen_ind=1,
        counter_id=seeded_data["counter_ids"]["quick_trans"],
    )
    _create_service_request(
        internal_nonqtxn_client,
        first_citizen["citizen_id"],
        service_id=seeded_data["service_ids"]["msp"],
        channel_id=seeded_data["channel_ids"]["email"],
        quantity=1,
    )
    assert_status(internal_nonqtxn_client.post(f"/citizens/{first_citizen['citizen_id']}/add_to_queue/"), 200)

    second_citizen = _create_citizen(internal_nonqtxn_client, 1, name="QT7 Second")
    _update_citizen(
        internal_nonqtxn_client,
        second_citizen["citizen_id"],
        citizen_name="QT7 Second",
        qt_xn_citizen_ind=0,
        counter_id=seeded_data["counter_ids"]["counter"],
    )
    _create_service_request(
        internal_nonqtxn_client,
        second_citizen["citizen_id"],
        service_id=seeded_data["service_ids"]["ptax"],
        channel_id=seeded_data["channel_ids"]["phone"],
        quantity=1,
    )
    assert_status(internal_nonqtxn_client.post(f"/citizens/{second_citizen['citizen_id']}/add_to_queue/"), 200)

    first_invite = internal_nonqtxn_client.post("/citizens/invite/", json={})
    assert_status(first_invite, 200)
    assert json_of(first_invite)["citizen"]["citizen_id"] == second_citizen["citizen_id"]
    assert_status(internal_nonqtxn_client.post(f"/citizens/{second_citizen['citizen_id']}/begin_service/"), 200)
    assert_status(internal_nonqtxn_client.post(f"/citizens/{second_citizen['citizen_id']}/finish_service/"), 200)

    second_invite = internal_nonqtxn_client.post("/citizens/invite/", json={})
    assert_status(second_invite, 200)
    assert json_of(second_invite)["citizen"]["citizen_id"] == first_citizen["citizen_id"]
    assert_status(internal_nonqtxn_client.post(f"/citizens/{first_citizen['citizen_id']}/citizen_left/"), 200)
    assert _queue_ids(internal_nonqtxn_client) == []
