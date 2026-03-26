import pytest

from app.tests.api_test_support import assert_status, json_of


pytestmark = [pytest.mark.contracts, pytest.mark.usefixtures("seeded_database")]


def test_health_and_readyz_endpoints(client):
    health_response = client.get("/api/v1/healthz/")
    ready_response = client.get("/api/v1/readyz/")

    assert_status(health_response, 200)
    assert_status(ready_response, 200)
    assert json_of(health_response)["message"] == "api is healthy"
    assert json_of(ready_response)["message"] == "api is ready"


def test_internal_contract_endpoints(internal_ga_client, seeded_data):
    del seeded_data

    channels_response = internal_ga_client.get("/channels/")
    categories_response = internal_ga_client.get("/categories/")
    services_response = internal_ga_client.get("/services/")
    offices_response = internal_ga_client.get("/offices/")
    rooms_response = internal_ga_client.get("/rooms/")
    invigilators_response = internal_ga_client.get("/invigilators/")
    exam_types_response = internal_ga_client.get("/exam_types/")
    csr_self_response = internal_ga_client.get("/csrs/me/")

    for response in (
        channels_response,
        categories_response,
        services_response,
        offices_response,
        rooms_response,
        invigilators_response,
        exam_types_response,
        csr_self_response,
    ):
        assert_status(response, 200)

    channels = json_of(channels_response)["channels"]
    categories = json_of(categories_response)["categories"]
    services = json_of(services_response)["services"]
    offices = json_of(offices_response)["offices"]
    rooms = json_of(rooms_response)["rooms"]
    invigilators = json_of(invigilators_response)["invigilators"]
    exam_types = json_of(exam_types_response)["exam_types"]
    csr_self = json_of(csr_self_response)

    assert any(channel["channel_name"] == "Phone" for channel in channels)
    assert any(category["service_name"] == "Property Tax" for category in categories)
    assert any(service["service_name"] == "Payment - MSP" for service in services)
    assert any(office["office_name"] == "Test Office" for office in offices)
    assert any(room["room_name"] == "Boardroom 1" for room in rooms)
    assert any(invigilator["invigilator_name"] == "Homer Simpson" for invigilator in invigilators)
    assert any(exam_type["exam_type_name"] for exam_type in exam_types)
    assert csr_self["csr"]["role"]["role_code"] == "GA"
    assert csr_self["csr"]["office"]["office_name"] == "Test Office"


def test_public_user_profile_contracts(public_client):
    create_response = public_client.post("/users/")
    assert_status(create_response, 200)

    created_user = json_of(create_response)[0]
    get_me_response = public_client.get("/users/me/")
    appointments_response = public_client.get("/users/appointments/")

    assert_status(get_me_response, 200)
    assert_status(appointments_response, 200)
    assert json_of(get_me_response)[0]["username"] == created_user["username"]
    assert "appointments" in json_of(appointments_response)
