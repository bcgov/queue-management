import pytest
from app.tests.api_test_support import (
    assert_json_response,
    create_draft_appointment,
    json_of,
    public_slot_payload,
)
from app.tests.auth.auth_support import configure_video_path, create_walkin_target

pytestmark = [pytest.mark.auth, pytest.mark.usefixtures("seeded_database")]


@pytest.mark.parametrize(
    ("path", "query", "expected_key"),
    [
        pytest.param("/healthz/", "", "message", id="GET /healthz/"),
        pytest.param("/readyz/", "", "message", id="GET /readyz/"),
        pytest.param("/offices/", "", "offices", id="GET /offices/"),
        pytest.param("/services/", "", "services", id="GET /services/"),
        pytest.param("/categories/", "", "categories", id="GET /categories/"),
    ],
)
def test_bare_client_can_access_simple_open_routes(
    bare_client, path, query, expected_key
):
    """Assert that explicitly open routes remain reachable without an authenticated identity."""
    response = bare_client.get(f"{path}{query}")

    assert_json_response(response, 200)
    assert expected_key in json_of(response)


def test_bare_client_can_access_logout_without_authentication(bare_client):
    """Assert that logout remains reachable without an authenticated identity."""
    response = bare_client.get("/logout/")

    assert response.status_code == 302, response.get_data(as_text=True)
    assert response.headers["Location"].endswith("/admin/")


def test_bare_client_can_access_smartboard_without_authentication(
    bare_client, seeded_data
):
    """Assert that the public smartboard endpoint remains reachable without authentication."""
    office_number = seeded_data["office_numbers"]["test_office"]
    response = bare_client.get(f"/smartboard/?office_number={office_number}")

    assert_json_response(response, 200)
    body = json_of(response)
    assert "office_type" in body
    assert "citizens" in body


def test_bare_client_can_access_smartboard_side_menu_without_authentication(
    bare_client, seeded_data
):
    """Assert that the smartboard side-menu endpoint remains publicly reachable."""
    office_number = seeded_data["office_numbers"]["test_office"]
    response = bare_client.get(f"/smardboard/side-menu/{office_number}")

    assert_json_response(response, 200)
    assert "office" in json_of(response)


def test_bare_client_can_access_public_video_manifest_without_authentication(
    bare_client, app, monkeypatch, seeded_data, tmp_path
):
    """Assert that public video lookup remains reachable without an authenticated identity."""
    office_number = seeded_data["office_numbers"]["test_office"]
    configure_video_path(app, monkeypatch, tmp_path, office_number=office_number)

    response = bare_client.get(f"/videofiles/{office_number}")

    assert_json_response(response, 200)
    assert json_of(response)["videourl"].endswith(".mp4")


def test_bare_client_can_access_slots_without_authentication(bare_client, seeded_data):
    """Assert that appointment slot discovery remains publicly reachable."""
    response = bare_client.get(
        f"/offices/{seeded_data['office_ids']['limited_office']}/slots/?service_id={seeded_data['service_ids']['limited_office_service']}"
    )

    assert_json_response(response, 200)
    assert json_of(response)


def test_bare_client_can_access_walkin_lookup_without_authentication(
    bare_client, internal_ga_client, seeded_data, app
):
    """Assert that walk-in queue lookups remain publicly reachable without authentication."""
    _citizen, walkin_id = create_walkin_target(app, internal_ga_client, seeded_data)

    response = bare_client.get(f"/citizen/all-walkin/{walkin_id}/")

    assert_json_response(response, 200)
    assert "citizen" in json_of(response)


def test_bare_client_can_access_waiting_queue_details_without_authentication(
    bare_client, seeded_data, app
):
    """Assert that waiting smartboard queue details remain publicly reachable."""
    office_number = seeded_data["office_numbers"]["test_office"]

    with app.app_context():
        from app.models.theq import Office
        from qsystem import db

        office = Office.find_by_id(seeded_data["office_ids"]["test_office"])
        office.currently_waiting = 0
        db.session.add(office)
        db.session.commit()

    response = bare_client.get(f"/smardboard/Q-details/waiting/{office_number}")

    assert_json_response(response, 200)
    assert "citizen_in_q" in json_of(response)


def test_bare_client_can_access_upcoming_queue_details_without_authentication(
    bare_client, seeded_data, app
):
    """Assert that upcoming smartboard queue details remain publicly reachable."""
    office_number = seeded_data["office_numbers"]["test_office"]

    with app.app_context():
        from app.models.theq import Office
        from qsystem import db

        office = Office.find_by_id(seeded_data["office_ids"]["test_office"])
        office.currently_waiting = 0
        db.session.add(office)
        db.session.commit()

    response = bare_client.get(f"/smardboard/Q-details/upcoming/{office_number}")

    assert_json_response(response, 200)
    assert "booked_not_checkin" in json_of(response)


def test_bare_client_can_create_a_draft_appointment_without_authentication(
    bare_client, seeded_data
):
    """Assert that draft appointments remain creatable before a user authenticates."""
    payload, _day_key, _slots = public_slot_payload(
        bare_client, seeded_data, minimum_slots=1
    )
    response = bare_client.post("/appointments/draft", json=payload)

    assert_json_response(response, 201)
    assert json_of(response)["appointment"]["is_draft"] is True


def test_bare_client_can_delete_a_draft_appointment_without_authentication(
    bare_client, seeded_data
):
    """Assert that draft appointments remain deletable without an authenticated identity."""
    draft = create_draft_appointment(bare_client, seeded_data)

    response = bare_client.delete(f"/appointments/draft/{draft['appointment_id']}/")

    assert response.status_code == 204, response.get_data(as_text=True)


def test_bare_client_can_flush_expired_drafts_without_authentication(bare_client):
    """Assert that draft flushing remains callable without an authenticated identity."""
    response = bare_client.post("/appointments/draft/flush")

    assert_json_response(response, 200)
    assert "deleted_draft_ids" in json_of(response)
