import pytest
from app.tests.api_test_support import (
    assert_json_response,
    assert_unauthorized,
    create_internal_appointment,
    create_public_user,
    json_of,
    public_slot_payload,
    slot_window_to_iso,
)
from app.tests.auth.auth_support import create_public_appointment

pytestmark = [pytest.mark.auth, pytest.mark.usefixtures("seeded_database")]


def test_bare_client_receives_401_for_mixed_role_appointment_create(
    bare_client, seeded_data
):
    """Assert that appointment creation still requires some authenticated role even though multiple roles are allowed."""
    payload, _day_key, _slots = public_slot_payload(
        bare_client, seeded_data, minimum_slots=1
    )
    response = bare_client.post("/appointments/", json=payload)

    assert_unauthorized(response)


def test_bare_client_receives_401_for_mixed_role_appointment_update(
    bare_client, internal_ga_client, seeded_data
):
    """Assert that appointment updates still reject unauthenticated callers."""
    appointment = create_internal_appointment(
        internal_ga_client, seeded_data, days_from_now=2
    )
    response = bare_client.put(
        f"/appointments/{appointment['appointment_id']}/", json={"comments": "No auth"}
    )

    assert_unauthorized(response)


def test_bare_client_receives_401_for_mixed_role_appointment_delete(
    bare_client, internal_ga_client, seeded_data
):
    """Assert that appointment deletion still rejects unauthenticated callers."""
    appointment = create_internal_appointment(
        internal_ga_client, seeded_data, days_from_now=2
    )
    response = bare_client.delete(f"/appointments/{appointment['appointment_id']}/")

    assert_unauthorized(response)


def test_internal_user_can_create_appointments_on_mixed_role_route(
    internal_ga_client, seeded_data
):
    """Assert that internal users can still create appointments on the shared appointment route."""
    appointment = create_internal_appointment(
        internal_ga_client, seeded_data, days_from_now=2
    )

    assert appointment["appointment_id"] > 0


def test_internal_user_can_update_appointments_on_mixed_role_route(
    internal_ga_client, seeded_data
):
    """Assert that internal users can still update appointments on the shared appointment route."""
    appointment = create_internal_appointment(
        internal_ga_client, seeded_data, days_from_now=2
    )

    response = internal_ga_client.put(
        f"/appointments/{appointment['appointment_id']}/",
        json={"comments": "Internal mixed-route update"},
    )

    assert_json_response(response, 200)
    assert json_of(response)["appointment"]["comments"] == "Internal mixed-route update"


def test_internal_user_can_delete_appointments_on_mixed_role_route(
    internal_ga_client, seeded_data
):
    """Assert that internal users can still delete appointments on the shared appointment route."""
    appointment = create_internal_appointment(
        internal_ga_client, seeded_data, days_from_now=2
    )

    response = internal_ga_client.delete(
        f"/appointments/{appointment['appointment_id']}/"
    )

    assert response.status_code == 204, response.get_data(as_text=True)


def test_public_user_can_create_appointments_on_mixed_role_route(
    public_client, seeded_data
):
    """Assert that public users can still create appointments on the shared appointment route."""
    create_public_user(public_client)
    payload, _day_key, _slots = public_slot_payload(
        public_client, seeded_data, minimum_slots=1
    )

    response = public_client.post("/appointments/", json=payload)

    assert_json_response(response, 201)
    assert json_of(response)["appointment"]["online_flag"] is True


def test_public_user_can_update_their_own_appointments_on_mixed_role_route(
    public_client, seeded_data
):
    """Assert that public users can still update their own appointments on the shared appointment route."""
    create_public_user(public_client)
    payload, day_key, slots = public_slot_payload(
        public_client, seeded_data, minimum_slots=2
    )
    create_response = public_client.post("/appointments/", json=payload)
    assert_json_response(create_response, 201)
    appointment = json_of(create_response)["appointment"]
    updated_start_time, updated_end_time = slot_window_to_iso(
        day_key,
        slots[1],
        seeded_data["office_timezones"]["limited_office"],
    )

    response = public_client.put(
        f"/appointments/{appointment['appointment_id']}/",
        json={
            "comments": "Public mixed-route update",
            "office_id": appointment["office_id"],
            "service_id": appointment["service_id"],
            "start_time": updated_start_time,
            "end_time": updated_end_time,
        },
    )

    assert_json_response(response, 200)
    assert json_of(response)["appointment"]["comments"] == "Public mixed-route update"


def test_public_user_can_delete_their_own_appointments_on_mixed_role_route(
    public_client, seeded_data
):
    """Assert that public users can still delete their own appointments on the shared appointment route."""
    appointment = create_public_appointment(public_client, seeded_data)

    response = public_client.delete(f"/appointments/{appointment['appointment_id']}/")

    assert response.status_code == 204, response.get_data(as_text=True)
