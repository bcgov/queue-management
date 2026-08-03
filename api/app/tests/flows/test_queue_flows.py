from __future__ import annotations

import pytest
from app.tests.api_test_support import (
    assert_json_response,
    json_of,
)
from app.tests.api_test_support import (
    create_citizen as _create_citizen,
)
from app.tests.api_test_support import (
    create_queue_ready_citizen as _create_queue_ready_citizen,
)
from app.tests.api_test_support import (
    create_service_ready_citizen as _create_service_ready_citizen,
)
from app.tests.api_test_support import (
    create_service_request as _create_service_request,
)
from app.tests.contracts.conftest import validate_schema
from app.tests.contracts.schemas import CITIZEN_RESPONSE_SCHEMA
from sqlalchemy.orm import raiseload

pytestmark = [pytest.mark.flows, pytest.mark.usefixtures("seeded_database")]


def _citizen_from_response(response, expected_status: int = 200):
    assert_json_response(response, expected_status)
    body = json_of(response)
    validate_schema(body, CITIZEN_RESPONSE_SCHEMA)
    return body["citizen"]


def _primary_service_request(citizen: dict) -> dict:
    return citizen["service_reqs"][0]


def _period_names(citizen: dict) -> list[str]:
    return [
        period["ps"]["ps_name"]
        for period in _primary_service_request(citizen)["periods"]
    ]


def _latest_period_name(record: dict) -> str:
    return record["periods"][-1]["ps"]["ps_name"]


def _assert_period_count_delta(record: dict, previous_count: int, *, delta: int = 1):
    assert len(record["periods"]) == previous_count + delta


def _queue_ids(api_client) -> list[int]:
    response = api_client.get("/citizens/")
    assert_json_response(response, 200)
    return [citizen["citizen_id"] for citizen in json_of(response)["citizens"]]


def test_qt1_specific_invite_appends_an_invited_period(internal_ga_client, seeded_data):
    """Assert that QT1 specific invites append an Invited period to the citizen's active request."""
    citizen, _service_request, queued_citizen = _create_queue_ready_citizen(
        internal_ga_client,
        seeded_data,
        position=0,
        name="QT1 Citizen",
        service_id_key="ptax",
        channel_id_key="phone",
        quantity=3,
        counter_id_key="counter",
        qt_xn_citizen_ind=0,
        comments="Needs property tax",
    )

    queued_period_count = len(_primary_service_request(queued_citizen)["periods"])
    invited_citizen = _citizen_from_response(
        internal_ga_client.post(f"/citizens/{citizen['citizen_id']}/invite/")
    )

    assert _latest_period_name(_primary_service_request(invited_citizen)) == "Invited"
    _assert_period_count_delta(
        _primary_service_request(invited_citizen), queued_period_count
    )


def test_generic_invite_accepts_an_empty_post_body(
    internal_ga_client, seeded_data
):
    """Assert that legacy empty-body invites still default to the CSR counter under Flask 3."""
    citizen, _service_request, queued_citizen = _create_queue_ready_citizen(
        internal_ga_client,
        seeded_data,
        position=0,
        name="Empty Body Invite Citizen",
        service_id_key="ptax",
        channel_id_key="phone",
        quantity=1,
        counter_id_key="counter",
        qt_xn_citizen_ind=0,
    )

    queued_period_count = len(_primary_service_request(queued_citizen)["periods"])
    invited_citizen = _citizen_from_response(
        internal_ga_client.post("/citizens/invite/", data="")
    )

    assert invited_citizen["citizen_id"] == citizen["citizen_id"]
    assert _latest_period_name(_primary_service_request(invited_citizen)) == "Invited"
    _assert_period_count_delta(
        _primary_service_request(invited_citizen), queued_period_count
    )


def test_qt1_begin_service_after_invite_appends_a_being_served_period(
    internal_ga_client, seeded_data
):
    """Assert that QT1 begin-service transitions append a Being Served period after a specific invite."""
    citizen, _service_request, _queued_citizen = _create_queue_ready_citizen(
        internal_ga_client,
        seeded_data,
        position=0,
        name="QT1 Citizen",
        service_id_key="ptax",
        channel_id_key="phone",
        quantity=3,
        counter_id_key="counter",
        qt_xn_citizen_ind=0,
        comments="Needs property tax",
    )

    invited_citizen = _citizen_from_response(
        internal_ga_client.post(f"/citizens/{citizen['citizen_id']}/invite/")
    )
    invited_period_count = len(_primary_service_request(invited_citizen)["periods"])
    serving_citizen = _citizen_from_response(
        internal_ga_client.post(f"/citizens/{citizen['citizen_id']}/begin_service/")
    )

    assert (
        _latest_period_name(_primary_service_request(serving_citizen)) == "Being Served"
    )
    _assert_period_count_delta(
        _primary_service_request(serving_citizen), invited_period_count
    )


def test_qt1_reactivate_service_request_restores_a_being_served_period(
    internal_ga_client, seeded_data
):
    """Assert that QT1 reactivation appends a fresh Being Served period to the original request."""
    citizen, first_service, _queued_citizen = _create_queue_ready_citizen(
        internal_ga_client,
        seeded_data,
        position=0,
        name="QT1 Citizen",
        service_id_key="ptax",
        channel_id_key="phone",
        quantity=3,
        counter_id_key="counter",
        qt_xn_citizen_ind=0,
        comments="Needs property tax",
    )

    _citizen_from_response(
        internal_ga_client.post(f"/citizens/{citizen['citizen_id']}/invite/")
    )
    serving_citizen = _citizen_from_response(
        internal_ga_client.post(f"/citizens/{citizen['citizen_id']}/begin_service/")
    )
    serving_period_count = len(_primary_service_request(serving_citizen)["periods"])

    second_service = _create_service_request(
        internal_ga_client,
        citizen["citizen_id"],
        service_id=seeded_data["service_ids"]["msp"],
        channel_id=seeded_data["channel_ids"]["email"],
        quantity=1,
    )
    reactivate_response = internal_ga_client.post(
        f"/service_requests/{first_service['sr_id']}/activate/"
    )

    assert_json_response(reactivate_response, 200)
    reactivated_request = json_of(reactivate_response)["service_request"]

    assert second_service["service_id"] == seeded_data["service_ids"]["msp"]
    assert reactivated_request["sr_id"] == first_service["sr_id"]
    assert _latest_period_name(reactivated_request) == "Being Served"
    _assert_period_count_delta(reactivated_request, serving_period_count)


def test_qt1_finish_service_completes_both_requests_and_clears_the_queue(
    internal_ga_client, seeded_data, app
):
    """Assert that QT1 finish-service completes both requests, updates citizen state, and clears the queue."""
    citizen, first_service, _queued_citizen = _create_queue_ready_citizen(
        internal_ga_client,
        seeded_data,
        position=0,
        name="QT1 Citizen",
        service_id_key="ptax",
        channel_id_key="phone",
        quantity=3,
        counter_id_key="counter",
        qt_xn_citizen_ind=0,
        comments="Needs property tax",
    )

    _citizen_from_response(
        internal_ga_client.post(f"/citizens/{citizen['citizen_id']}/invite/")
    )
    _citizen_from_response(
        internal_ga_client.post(f"/citizens/{citizen['citizen_id']}/begin_service/")
    )
    _create_service_request(
        internal_ga_client,
        citizen["citizen_id"],
        service_id=seeded_data["service_ids"]["msp"],
        channel_id=seeded_data["channel_ids"]["email"],
        quantity=1,
    )
    assert_json_response(
        internal_ga_client.post(
            f"/service_requests/{first_service['sr_id']}/activate/"
        ),
        200,
    )

    finished_citizen = _citizen_from_response(
        internal_ga_client.post(f"/citizens/{citizen['citizen_id']}/finish_service/")
    )

    assert [
        service_request["sr_state"]["sr_code"]
        for service_request in finished_citizen["service_reqs"]
    ] == [
        "Complete",
        "Complete",
    ]
    assert finished_citizen["cs"]["cs_state_name"] == "Received Services"
    assert _queue_ids(internal_ga_client) == []

    with app.app_context():
        from app.models.theq import Citizen, ServiceReq

        citizen_model = Citizen.query.filter_by(
            citizen_id=citizen["citizen_id"]
        ).first()
        sr_models = (
            ServiceReq.query.filter_by(citizen_id=citizen["citizen_id"])
            .order_by(ServiceReq.sr_number)
            .all()
        )
        assert citizen_model.cs.cs_state_name == "Received Services"
        assert [service_request.sr_state.sr_code for service_request in sr_models] == [
            "Complete",
            "Complete",
        ]


def test_qt2_begin_service_appends_a_being_served_period(
    internal_ga_client, seeded_data
):
    """Assert that QT2 begin-service appends a Being Served period to the active request."""
    citizen, service_request = _create_service_ready_citizen(
        internal_ga_client,
        seeded_data,
        position=0,
        name="QT2 Citizen",
        service_id_key="ptax",
        channel_id_key="phone",
        quantity=2,
        counter_id_key="counter",
    )

    initial_period_count = len(service_request["periods"])
    serving_citizen = _citizen_from_response(
        internal_ga_client.post(f"/citizens/{citizen['citizen_id']}/begin_service/")
    )

    assert (
        _latest_period_name(_primary_service_request(serving_citizen)) == "Being Served"
    )
    _assert_period_count_delta(
        _primary_service_request(serving_citizen), initial_period_count
    )


def test_qt2_place_on_hold_appends_an_on_hold_period(internal_ga_client, seeded_data):
    """Assert that QT2 place-on-hold appends an On hold period to the active request."""
    citizen, _service_request = _create_service_ready_citizen(
        internal_ga_client,
        seeded_data,
        position=0,
        name="QT2 Citizen",
        service_id_key="ptax",
        channel_id_key="phone",
        quantity=2,
        counter_id_key="counter",
    )

    serving_citizen = _citizen_from_response(
        internal_ga_client.post(f"/citizens/{citizen['citizen_id']}/begin_service/")
    )
    serving_period_count = len(_primary_service_request(serving_citizen)["periods"])
    held_citizen = _citizen_from_response(
        internal_ga_client.post(f"/citizens/{citizen['citizen_id']}/place_on_hold/")
    )

    assert _latest_period_name(_primary_service_request(held_citizen)) == "On hold"
    _assert_period_count_delta(
        _primary_service_request(held_citizen), serving_period_count
    )


def test_qt2_resume_service_appends_being_served_after_hold(
    internal_ga_client, seeded_data
):
    """Assert that QT2 resume transitions append Being Served after the existing hold history."""
    citizen, _service_request = _create_service_ready_citizen(
        internal_ga_client,
        seeded_data,
        position=0,
        name="QT2 Citizen",
        service_id_key="ptax",
        channel_id_key="phone",
        quantity=2,
        counter_id_key="counter",
    )

    _citizen_from_response(
        internal_ga_client.post(f"/citizens/{citizen['citizen_id']}/begin_service/")
    )
    held_citizen = _citizen_from_response(
        internal_ga_client.post(f"/citizens/{citizen['citizen_id']}/place_on_hold/")
    )
    held_period_count = len(_primary_service_request(held_citizen)["periods"])
    resumed_citizen = _citizen_from_response(
        internal_ga_client.post(f"/citizens/{citizen['citizen_id']}/begin_service/")
    )

    assert (
        _latest_period_name(_primary_service_request(resumed_citizen)) == "Being Served"
    )
    _assert_period_count_delta(
        _primary_service_request(resumed_citizen), held_period_count
    )
    assert _period_names(resumed_citizen)[-3:] == [
        "Being Served",
        "On hold",
        "Being Served",
    ]


def test_qt2_finish_service_marks_the_request_complete_and_clears_the_queue(
    internal_ga_client, seeded_data
):
    """Assert that QT2 finish-service leaves the request Complete and removes the citizen from the queue."""
    citizen, _service_request = _create_service_ready_citizen(
        internal_ga_client,
        seeded_data,
        position=0,
        name="QT2 Citizen",
        service_id_key="ptax",
        channel_id_key="phone",
        quantity=2,
        counter_id_key="counter",
    )

    _citizen_from_response(
        internal_ga_client.post(f"/citizens/{citizen['citizen_id']}/begin_service/")
    )
    _citizen_from_response(
        internal_ga_client.post(f"/citizens/{citizen['citizen_id']}/place_on_hold/")
    )
    _citizen_from_response(
        internal_ga_client.post(f"/citizens/{citizen['citizen_id']}/begin_service/")
    )
    finished_citizen = _citizen_from_response(
        internal_ga_client.post(f"/citizens/{citizen['citizen_id']}/finish_service/")
    )

    assert (
        _primary_service_request(finished_citizen)["sr_state"]["sr_code"] == "Complete"
    )
    assert _queue_ids(internal_ga_client) == []


def test_qt3_citizen_leaves_after_create(internal_ga_client, app):
    """Assert that QT3 marks a newly created citizen as having left before service."""
    citizen = _create_citizen(internal_ga_client, 0, name="QT3 Citizen")
    leave_response = internal_ga_client.post(
        f"/citizens/{citizen['citizen_id']}/citizen_left/"
    )

    assert_json_response(leave_response, 200)

    with app.app_context():
        from app.models.theq import Citizen

        citizen_model = Citizen.query.filter_by(
            citizen_id=citizen["citizen_id"]
        ).first()
        assert citizen_model.cs.cs_state_name == "Left before receiving services"


def test_qt4_citizen_leaves_after_waiting(internal_ga_client, seeded_data, app):
    """Assert that QT4 preserves the left-state transition after the citizen joins the queue."""
    citizen, _service_request, _queued_citizen = _create_queue_ready_citizen(
        internal_ga_client,
        seeded_data,
        position=0,
        name="QT4 Citizen",
        service_id_key="ptax",
        channel_id_key="phone",
        quantity=1,
        counter_id_key="counter",
        qt_xn_citizen_ind=0,
    )
    leave_response = internal_ga_client.post(
        f"/citizens/{citizen['citizen_id']}/citizen_left/"
    )

    assert_json_response(leave_response, 200)

    with app.app_context():
        from app.models.theq import Citizen

        citizen_model = Citizen.query.filter_by(
            citizen_id=citizen["citizen_id"]
        ).first()
        assert citizen_model.cs.cs_state_name == "Left before receiving services"


def test_qt5_update_service_request_quantity_and_service(
    internal_ga_client, seeded_data, app
):
    """Assert that QT5 preserves service-request updates while a citizen is being served."""
    citizen, service_request = _create_service_ready_citizen(
        internal_ga_client,
        seeded_data,
        position=0,
        name="QT5 Citizen",
        service_id_key="ptax",
        channel_id_key="phone",
        quantity=3,
    )
    _citizen_from_response(
        internal_ga_client.post(f"/citizens/{citizen['citizen_id']}/begin_service/")
    )

    quantity_update = internal_ga_client.put(
        f"/service_requests/{service_request['sr_id']}/", json={"quantity": 5}
    )
    service_update = internal_ga_client.put(
        f"/service_requests/{service_request['sr_id']}/",
        json={"service_id": seeded_data["service_ids"]["msp"]},
    )
    finish_response = internal_ga_client.post(
        f"/citizens/{citizen['citizen_id']}/finish_service/"
    )

    assert_json_response(quantity_update, 200)
    assert json_of(quantity_update)["service_request"]["quantity"] == 5
    assert_json_response(service_update, 200)
    assert (
        json_of(service_update)["service_request"]["service_id"]
        == seeded_data["service_ids"]["msp"]
    )
    assert_json_response(finish_response, 200)

    with app.app_context():
        from app.models.theq import ServiceReq

        service_request_model = ServiceReq.query.filter_by(
            sr_id=service_request["sr_id"]
        ).first()
        assert service_request_model.quantity == 5
        assert service_request_model.service_id == seeded_data["service_ids"]["msp"]


def test_qt6_first_generic_invite_prefers_the_quick_transaction_counter(
    internal_ga_client, seeded_data
):
    """Assert that QT6 generic invite selects the quick-transaction citizen before the standard queue."""
    _first_citizen, _first_service_request, _first_queued_citizen = (
        _create_queue_ready_citizen(
            internal_ga_client,
            seeded_data,
            position=0,
            name="QT6 First",
            service_id_key="ptax",
            channel_id_key="phone",
            quantity=1,
            counter_id_key="counter",
            qt_xn_citizen_ind=0,
        )
    )
    second_citizen, _second_service_request, second_queued_citizen = (
        _create_queue_ready_citizen(
            internal_ga_client,
            seeded_data,
            position=1,
            name="QT6 Second",
            service_id_key="msp",
            channel_id_key="email",
            quantity=1,
            counter_id_key="quick_trans",
            qt_xn_citizen_ind=1,
        )
    )

    queued_period_count = len(
        _primary_service_request(second_queued_citizen)["periods"]
    )
    invited_citizen = _citizen_from_response(
        internal_ga_client.post("/citizens/invite/", json={})
    )

    assert invited_citizen["citizen_id"] == second_citizen["citizen_id"]
    assert invited_citizen["qt_xn_citizen_ind"] == 1
    assert _latest_period_name(_primary_service_request(invited_citizen)) == "Invited"
    _assert_period_count_delta(
        _primary_service_request(invited_citizen), queued_period_count
    )


def test_generic_invite_snowplow_context_handles_raiseloaded_citizen(
    internal_ga_client, seeded_data, app
):
    """Assert that SnowPlow can build citizen context from the generic invite query shape."""
    citizen, _service_request, _queued_citizen = _create_queue_ready_citizen(
        internal_ga_client,
        seeded_data,
        position=0,
        name="SnowPlow Generic Invite Citizen",
        service_id_key="ptax",
        channel_id_key="phone",
        quantity=1,
        counter_id_key="quick_trans",
        qt_xn_citizen_ind=1,
    )

    with app.app_context():
        from app.models.theq import Citizen
        from app.utilities.snowplow import SnowPlow

        citizen_model = (
            Citizen.query.options(
                raiseload(Citizen.office),
                raiseload(Citizen.counter),
                raiseload(Citizen.user),
            )
            .filter_by(citizen_id=citizen["citizen_id"])
            .first()
        )

        citizen_context = SnowPlow.get_citizen(
            citizen_model,
            "Counter",
            svc_number=3,
        )

        assert citizen_context.data == {
            "client_id": citizen["citizen_id"],
            "service_count": 3,
            "counter_type": "Quick Trans",
        }


def test_qt6_second_generic_invite_returns_the_remaining_standard_queue_citizen(
    internal_ga_client, seeded_data
):
    """Assert that QT6 returns the remaining standard-queue citizen after the quick-transaction citizen finishes."""
    first_citizen, _first_service_request, first_queued_citizen = (
        _create_queue_ready_citizen(
            internal_ga_client,
            seeded_data,
            position=0,
            name="QT6 First",
            service_id_key="ptax",
            channel_id_key="phone",
            quantity=1,
            counter_id_key="counter",
            qt_xn_citizen_ind=0,
        )
    )
    second_citizen, _second_service_request, _second_queued_citizen = (
        _create_queue_ready_citizen(
            internal_ga_client,
            seeded_data,
            position=1,
            name="QT6 Second",
            service_id_key="msp",
            channel_id_key="email",
            quantity=1,
            counter_id_key="quick_trans",
            qt_xn_citizen_ind=1,
        )
    )

    first_invited_citizen = _citizen_from_response(
        internal_ga_client.post("/citizens/invite/", json={})
    )
    _citizen_from_response(
        internal_ga_client.post(
            f"/citizens/{second_citizen['citizen_id']}/begin_service/"
        )
    )
    _citizen_from_response(
        internal_ga_client.post(
            f"/citizens/{second_citizen['citizen_id']}/finish_service/"
        )
    )

    queued_period_count = len(_primary_service_request(first_queued_citizen)["periods"])
    second_invited_citizen = _citizen_from_response(
        internal_ga_client.post("/citizens/invite/", json={})
    )

    assert first_invited_citizen["citizen_id"] == second_citizen["citizen_id"]
    assert second_invited_citizen["citizen_id"] == first_citizen["citizen_id"]
    assert second_invited_citizen["qt_xn_citizen_ind"] == 0
    assert (
        _latest_period_name(_primary_service_request(second_invited_citizen))
        == "Invited"
    )
    _assert_period_count_delta(
        _primary_service_request(second_invited_citizen), queued_period_count
    )

    assert_json_response(
        internal_ga_client.post(
            f"/citizens/{first_citizen['citizen_id']}/citizen_left/"
        ),
        200,
    )
    assert _queue_ids(internal_ga_client) == []


def test_qt7_first_generic_invite_prefers_the_standard_counter(
    internal_nonqtxn_client, seeded_data
):
    """Assert that QT7 generic invite selects the standard-queue citizen for a non-quick-transaction CSR."""
    first_citizen, _first_service_request, first_queued_citizen = (
        _create_queue_ready_citizen(
            internal_nonqtxn_client,
            seeded_data,
            position=0,
            name="QT7 First",
            service_id_key="ptax",
            channel_id_key="phone",
            quantity=1,
            counter_id_key="counter",
            qt_xn_citizen_ind=0,
        )
    )
    _second_citizen, _second_service_request, _second_queued_citizen = (
        _create_queue_ready_citizen(
            internal_nonqtxn_client,
            seeded_data,
            position=1,
            name="QT7 Second",
            service_id_key="msp",
            channel_id_key="email",
            quantity=1,
            counter_id_key="quick_trans",
            qt_xn_citizen_ind=1,
        )
    )

    queued_period_count = len(_primary_service_request(first_queued_citizen)["periods"])
    invited_citizen = _citizen_from_response(
        internal_nonqtxn_client.post("/citizens/invite/", json={})
    )

    assert invited_citizen["citizen_id"] == first_citizen["citizen_id"]
    assert invited_citizen["qt_xn_citizen_ind"] == 0
    assert _latest_period_name(_primary_service_request(invited_citizen)) == "Invited"
    _assert_period_count_delta(
        _primary_service_request(invited_citizen), queued_period_count
    )


def test_qt7_second_generic_invite_returns_the_remaining_quick_transaction_citizen(
    internal_nonqtxn_client, seeded_data
):
    """Assert that QT7 returns the remaining quick-transaction citizen after the standard citizen finishes."""
    first_citizen, _first_service_request, _first_queued_citizen = (
        _create_queue_ready_citizen(
            internal_nonqtxn_client,
            seeded_data,
            position=0,
            name="QT7 First",
            service_id_key="ptax",
            channel_id_key="phone",
            quantity=1,
            counter_id_key="counter",
            qt_xn_citizen_ind=0,
        )
    )
    second_citizen, _second_service_request, second_queued_citizen = (
        _create_queue_ready_citizen(
            internal_nonqtxn_client,
            seeded_data,
            position=1,
            name="QT7 Second",
            service_id_key="msp",
            channel_id_key="email",
            quantity=1,
            counter_id_key="quick_trans",
            qt_xn_citizen_ind=1,
        )
    )

    first_invited_citizen = _citizen_from_response(
        internal_nonqtxn_client.post("/citizens/invite/", json={})
    )
    _citizen_from_response(
        internal_nonqtxn_client.post(
            f"/citizens/{first_citizen['citizen_id']}/begin_service/"
        )
    )
    _citizen_from_response(
        internal_nonqtxn_client.post(
            f"/citizens/{first_citizen['citizen_id']}/finish_service/"
        )
    )

    queued_period_count = len(
        _primary_service_request(second_queued_citizen)["periods"]
    )
    second_invited_citizen = _citizen_from_response(
        internal_nonqtxn_client.post("/citizens/invite/", json={})
    )

    assert first_invited_citizen["citizen_id"] == first_citizen["citizen_id"]
    assert second_invited_citizen["citizen_id"] == second_citizen["citizen_id"]
    assert second_invited_citizen["qt_xn_citizen_ind"] == 1
    assert (
        _latest_period_name(_primary_service_request(second_invited_citizen))
        == "Invited"
    )
    _assert_period_count_delta(
        _primary_service_request(second_invited_citizen), queued_period_count
    )

    assert_json_response(
        internal_nonqtxn_client.post(
            f"/citizens/{second_citizen['citizen_id']}/citizen_left/"
        ),
        200,
    )
    assert _queue_ids(internal_nonqtxn_client) == []
