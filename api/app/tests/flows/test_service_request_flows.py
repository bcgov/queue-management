from __future__ import annotations

import re

import pytest
from app.tests.api_test_support import (
    assert_json_response,
    create_citizen,
    create_service_ready_citizen,
    json_of,
)

pytestmark = [pytest.mark.flows, pytest.mark.usefixtures("seeded_database")]


def _service_request_payload(
    citizen_id: int,
    seeded_data,
    *,
    service_id: int,
    channel_id_key: str = "phone",
    quantity: int = 1,
):
    return {
        "service_request": {
            "citizen_id": citizen_id,
            "service_id": service_id,
            "channel_id": seeded_data["channel_ids"][channel_id_key],
            "quantity": quantity,
        }
    }


def test_service_request_create_rejects_missing_payload(internal_ga_client):
    """Assert that the create endpoint returns a stable 400 when JSON input is missing."""
    response = internal_ga_client.post(
        "/service_requests/",
        data="null",
        content_type="application/json",
    )

    assert response.status_code == 400, response.get_data(as_text=True)
    assert json_of(response)["message"] == "No input data received for creating service request"


def test_service_request_create_rejects_category_selection(
    internal_ga_client, seeded_data
):
    """Assert that category ids are rejected so the frontend must submit a concrete service."""
    citizen = create_citizen(internal_ga_client, 0, name="Category Rejection Citizen")
    response = internal_ga_client.post(
        "/service_requests/",
        json=_service_request_payload(
            citizen["citizen_id"],
            seeded_data,
            service_id=seeded_data["service_ids"]["ptax_category"],
        ),
    )

    assert response.status_code == 400, response.get_data(as_text=True)
    assert "category" in json_of(response)["message"].lower()


def test_first_service_request_assigns_ticket_numbers_and_choose_service_event(
    internal_ga_client, seeded_data, app, monkeypatch
):
    """Assert that the first service request creates a ticket number and emits only the choose-service event."""
    from app.resources.theq import service_requests_list as service_requests_module

    choose_service_calls = []
    snowplow_events = []
    monkeypatch.setattr(
        service_requests_module.SnowPlow,
        "choose_service",
        staticmethod(
            lambda service_request, csr, event: choose_service_calls.append(
                (service_request.sr_number, csr.username, event)
            )
        ),
    )
    monkeypatch.setattr(
        service_requests_module.SnowPlow,
        "snowplow_event",
        staticmethod(
            lambda citizen_id, csr, event, current_sr_number=None: snowplow_events.append(
                (citizen_id, csr.username, event, current_sr_number)
            )
        ),
    )

    citizen = create_citizen(internal_ga_client, 0, name="First Service Citizen")
    response = internal_ga_client.post(
        "/service_requests/",
        json=_service_request_payload(
            citizen["citizen_id"],
            seeded_data,
            service_id=seeded_data["service_ids"]["ptax"],
        ),
    )
    body = json_of(response)

    assert_json_response(response, 201)
    assert body["service_request"]["sr_number"] == 1
    assert choose_service_calls == [(1, "cfms-postman-operator", "chooseservice")]
    assert snowplow_events == []

    with app.app_context():
        from app.models.theq import Citizen, Service

        citizen_model = Citizen.find_citizen_by_id(citizen["citizen_id"])
        service = Service.query.filter_by(service_id=seeded_data["service_ids"]["ptax"]).first()

        assert citizen_model.cs.cs_state_name == "Active"
        assert citizen_model.ticket_number.startswith(service.prefix)
        assert re.fullmatch(rf"{re.escape(service.prefix)}\d+", citizen_model.ticket_number)


def test_additional_service_request_completes_the_previous_request_and_emits_transition_events(
    internal_ga_client, seeded_data, app, monkeypatch
):
    """Assert that adding a second service closes the active request and emits the stop/additional Snowplow events."""
    from app.resources.theq import service_requests_list as service_requests_module

    choose_service_calls = []
    snowplow_events = []
    monkeypatch.setattr(
        service_requests_module.SnowPlow,
        "choose_service",
        staticmethod(
            lambda service_request, csr, event: choose_service_calls.append(
                (service_request.sr_number, event)
            )
        ),
    )
    monkeypatch.setattr(
        service_requests_module.SnowPlow,
        "snowplow_event",
        staticmethod(
            lambda citizen_id, csr, event, current_sr_number=None: snowplow_events.append(
                (event, current_sr_number)
            )
        ),
    )

    citizen, first_service = create_service_ready_citizen(
        internal_ga_client,
        seeded_data,
        position=0,
        name="Additional Service Citizen",
        service_id_key="ptax",
        channel_id_key="phone",
        quantity=1,
    )
    choose_service_calls.clear()
    snowplow_events.clear()

    response = internal_ga_client.post(
        "/service_requests/",
        json=_service_request_payload(
            citizen["citizen_id"],
            seeded_data,
            service_id=seeded_data["service_ids"]["msp"],
            channel_id_key="email",
        ),
    )
    body = json_of(response)

    assert_json_response(response, 201)
    assert body["service_request"]["sr_number"] == 2
    assert choose_service_calls == [(2, "chooseservice")]
    assert snowplow_events == [("stopservice", 1), ("additionalservice", 2)]

    with app.app_context():
        from app.models.theq import ServiceReq

        requests = (
            ServiceReq.query.filter_by(citizen_id=citizen["citizen_id"])
            .order_by(ServiceReq.sr_number)
            .all()
        )

        assert first_service["sr_id"] == requests[0].sr_id
        assert [request.sr_state.sr_code for request in requests] == ["Complete", "Active"]
        assert requests[1].sr_number == 2
