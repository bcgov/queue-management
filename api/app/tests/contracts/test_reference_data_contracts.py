from datetime import datetime, timezone

import pytest
from app.tests.api_test_support import assert_json_response, json_of
from app.tests.contracts.conftest import validate_schema
from app.tests.contracts.schemas import (
    CATEGORY_LIST_RESPONSE_SCHEMA,
    CSR_LIST_RESPONSE_SCHEMA,
    CHANNEL_LIST_RESPONSE_SCHEMA,
    CSR_ME_RESPONSE_SCHEMA,
    EXAM_TYPE_LIST_RESPONSE_SCHEMA,
    INVIGILATOR_LIST_RESPONSE_SCHEMA,
    OFFICE_LIST_RESPONSE_SCHEMA,
    ROOM_LIST_RESPONSE_SCHEMA,
    SMARTBOARD_SIDE_MENU_RESPONSE_SCHEMA,
    SERVICE_LIST_RESPONSE_SCHEMA,
)
from app.tests.auth.auth_support import promote_internal_csr_to_support

pytestmark = [pytest.mark.contracts, pytest.mark.usefixtures("seeded_database")]


def test_channels_contract_includes_named_channels(internal_ga_client):
    """Assert that channels expose the stable identifier and display-name fields."""
    response = internal_ga_client.get("/channels/")
    body = json_of(response)

    assert_json_response(response, 200)
    validate_schema(body, CHANNEL_LIST_RESPONSE_SCHEMA)
    assert any(channel["channel_name"] == "Phone" for channel in body["channels"])


def test_categories_contract_includes_dashboard_flags(internal_ga_client):
    """Assert that category responses preserve the frontend flag fields and parent reference."""
    response = internal_ga_client.get("/categories/")
    body = json_of(response)

    assert_json_response(response, 200)
    validate_schema(body, CATEGORY_LIST_RESPONSE_SCHEMA)

    property_tax = next(
        category
        for category in body["categories"]
        if category["service_name"] == "Property Tax"
    )
    assert property_tax["actual_service_ind"] == 0
    assert "display_dashboard_ind" in property_tax
    assert property_tax["parent_id"] is None


def test_services_contract_includes_parent_relationships(internal_ga_client):
    """Assert that services expose parent relationships needed for service selection UIs."""
    response = internal_ga_client.get("/services/")
    body = json_of(response)

    assert_json_response(response, 200)
    validate_schema(body, SERVICE_LIST_RESPONSE_SCHEMA)

    service = next(
        service
        for service in body["services"]
        if service["service_name"] == "Payment - MSP"
    )
    assert service["parent_id"] is not None
    assert service["parent"]["service_name"]

    rural_ptax = next(
        service
        for service in body["services"]
        if service["service_name"] == "Other - Rural PTAX"
    )
    assert rural_ptax["parent"]["service_name"] == "Property Tax"


def test_office_scoped_services_filter_deleted_entries_and_preserve_sort_order(
    internal_ga_client, seeded_data, app
):
    """Assert that office-scoped services stay filtered and stably ordered for service-picking UIs."""
    with app.app_context():
        from app.models.theq import Office, Service
        from qsystem import db

        test_office = Office.find_by_id(seeded_data["office_ids"]["test_office"])
        limited_office = Office.find_by_id(seeded_data["office_ids"]["limited_office"])

        ordered_parent = Service(
            service_code="ORDERED-CATEGORY",
            service_name="Ordered Category",
            service_desc="Ordered category for scoped services tests",
            prefix="O",
            display_dashboard_ind=0,
            actual_service_ind=0,
        )
        alpha_child = Service(
            service_code="ORDERED-ALPHA",
            service_name="Alpha Child",
            service_desc="Alpha child service",
            prefix="O",
            display_dashboard_ind=1,
            actual_service_ind=1,
            parent=ordered_parent,
        )
        zebra_child = Service(
            service_code="ORDERED-ZEBRA",
            service_name="Zebra Child",
            service_desc="Zebra child service",
            prefix="O",
            display_dashboard_ind=1,
            actual_service_ind=1,
            parent=ordered_parent,
        )
        deleted_child = Service(
            service_code="ORDERED-DELETED",
            service_name="Deleted Child",
            service_desc="Deleted child service",
            prefix="O",
            display_dashboard_ind=1,
            actual_service_ind=1,
            parent=ordered_parent,
            deleted=datetime.now(timezone.utc),
        )
        other_office_only = Service(
            service_code="ORDERED-OTHER",
            service_name="Other Office Only",
            service_desc="Service available only in the limited office",
            prefix="O",
            display_dashboard_ind=1,
            actual_service_ind=1,
            parent=ordered_parent,
        )

        db.session.add_all(
            [
                ordered_parent,
                alpha_child,
                zebra_child,
                deleted_child,
                other_office_only,
            ]
        )
        db.session.flush()

        test_office.services.extend(
            [ordered_parent, alpha_child, zebra_child, deleted_child]
        )
        limited_office.services.append(other_office_only)
        db.session.add_all([test_office, limited_office])
        db.session.commit()

    response = internal_ga_client.get(
        f"/services/?office_id={seeded_data['office_ids']['test_office']}"
    )
    body = json_of(response)

    assert_json_response(response, 200)
    validate_schema(body, SERVICE_LIST_RESPONSE_SCHEMA)

    service_names = [service["service_name"] for service in body["services"]]
    assert "Deleted Child" not in service_names
    assert "Other Office Only" not in service_names
    assert service_names.index("Ordered Category") < service_names.index("Alpha Child")
    assert service_names.index("Alpha Child") < service_names.index("Zebra Child")


def test_offices_contract_includes_timezone_counters_and_timeslots(internal_ga_client):
    """Assert that office responses preserve nested timezone, counter, and timeslot data."""
    response = internal_ga_client.get("/offices/")
    body = json_of(response)

    assert_json_response(response, 200)
    validate_schema(body, OFFICE_LIST_RESPONSE_SCHEMA)

    office = next(
        office for office in body["offices"] if office["office_name"] == "Test Office"
    )
    assert office["timezone"]["timezone_name"]
    assert office["counters"]
    assert "timeslots" in office


def test_rooms_contract_includes_room_metadata(internal_ga_client):
    """Assert that room responses preserve the room metadata needed by booking screens."""
    response = internal_ga_client.get("/rooms/")
    body = json_of(response)

    assert_json_response(response, 200)
    validate_schema(body, ROOM_LIST_RESPONSE_SCHEMA)
    assert any(room["room_name"] == "Boardroom 1" for room in body["rooms"])


def test_rooms_contract_can_be_scoped_to_an_office_and_excludes_deleted_rooms(
    internal_ga_client, seeded_data, app
):
    """Assert that room-list filtering keeps only active rooms for the selected office."""
    with app.app_context():
        from app.models.bookings import Room
        from qsystem import db

        db.session.add_all(
            [
                Room(
                    office_id=seeded_data["office_ids"]["test_office"],
                    room_name="Scoped Contract Room",
                    capacity=4,
                    color="#00AA66",
                ),
                Room(
                    office_id=seeded_data["office_ids"]["limited_office"],
                    room_name="Other Office Room",
                    capacity=4,
                    color="#AA6600",
                ),
                Room(
                    office_id=seeded_data["office_ids"]["test_office"],
                    room_name="Deleted Contract Room",
                    capacity=4,
                    color="#AA0066",
                    deleted=datetime.now(timezone.utc),
                ),
            ]
        )
        db.session.commit()

    response = internal_ga_client.get(
        f"/rooms/?office_id={seeded_data['office_ids']['test_office']}"
    )
    body = json_of(response)

    assert_json_response(response, 200)
    validate_schema(body, ROOM_LIST_RESPONSE_SCHEMA)

    room_names = [room["room_name"] for room in body["rooms"]]
    assert "Scoped Contract Room" in room_names
    assert "Other Office Room" not in room_names
    assert "Deleted Contract Room" not in room_names


def test_invigilators_contract_includes_shadow_flags(internal_ga_client):
    """Assert that invigilator responses preserve shadow-count and contact fields."""
    response = internal_ga_client.get("/invigilators/")
    body = json_of(response)

    assert_json_response(response, 200)
    validate_schema(body, INVIGILATOR_LIST_RESPONSE_SCHEMA)

    invigilator = next(
        invigilator
        for invigilator in body["invigilators"]
        if invigilator["invigilator_name"] == "Homer Simpson"
    )
    assert invigilator["shadow_count"] == 2
    assert invigilator["shadow_flag"] == "Y"


def test_invigilators_offsite_contract_is_scoped_to_the_pesticide_office(
    internal_ga_client, seeded_data
):
    """Assert that the offsite invigilator payload stays limited to the pesticide office."""
    response = internal_ga_client.get("/invigilators/offsite/")
    body = json_of(response)

    assert_json_response(response, 200)
    validate_schema(body, INVIGILATOR_LIST_RESPONSE_SCHEMA)

    names = {invigilator["invigilator_name"] for invigilator in body["invigilators"]}
    assert names >= {"Pest 1", "Pest 2"}
    assert "Homer Simpson" not in names
    assert all(
        invigilator["office_id"] == seeded_data["office_ids"]["pesticide_office"]
        for invigilator in body["invigilators"]
    )


def test_exam_types_contract_includes_duration_and_group_flags(internal_ga_client):
    """Assert that exam-type responses preserve duration and grouping metadata."""
    response = internal_ga_client.get("/exam_types/")
    body = json_of(response)

    assert_json_response(response, 200)
    validate_schema(body, EXAM_TYPE_LIST_RESPONSE_SCHEMA)
    assert any(exam_type["exam_type_name"] for exam_type in body["exam_types"])


def test_csrs_contract_filters_deleted_users(internal_ga_client, app):
    """Assert that the CSR list keeps stable fields while excluding deleted users."""
    with app.app_context():
        from app.models.theq import CSR
        from qsystem import db

        csr = CSR.query.filter_by(username="cfms-postman-non-operator").first()
        csr.deleted = datetime.now(timezone.utc)
        db.session.add(csr)
        db.session.commit()

    response = internal_ga_client.get("/csrs/")
    body = json_of(response)

    assert_json_response(response, 200)
    validate_schema(body, CSR_LIST_RESPONSE_SCHEMA)

    usernames = {csr["username"] for csr in body["csrs"]}
    assert "cfms-postman-operator" in usernames
    assert "cfms-postman-non-operator" not in usernames


def test_csrs_contract_allows_support_but_rejects_other_internal_roles(
    internal_ga_client, internal_nonqtxn_client, app
):
    """Assert that only GA and SUPPORT users can reach the office CSR list."""
    forbidden_response = internal_nonqtxn_client.get("/csrs/")
    assert forbidden_response.status_code == 403

    promote_internal_csr_to_support(app, username="cfms-postman-operator")
    response = internal_ga_client.get("/csrs/")
    body = json_of(response)

    assert_json_response(response, 200)
    validate_schema(body, CSR_LIST_RESPONSE_SCHEMA)
    assert any(csr["role"]["role_code"] == "SUPPORT" for csr in body["csrs"])


def test_csr_me_contract_includes_role_office_and_designate_flags(internal_ga_client):
    """Assert that the csr-self payload preserves nested office and designate flag fields."""
    response = internal_ga_client.get("/csrs/me/")
    body = json_of(response)

    assert_json_response(response, 200)
    validate_schema(body, CSR_ME_RESPONSE_SCHEMA)

    csr = body["csr"]
    assert csr["role"]["role_code"] == "GA"
    assert csr["office"]["office_name"] == "Test Office"
    assert "finance_designate" in csr
    assert "ita2_designate" in csr
    assert "pesticide_designate" in csr


def test_smartboard_side_menu_contract_returns_the_frontend_office_payload(
    bare_client, seeded_data
):
    """Assert that the smartboard side menu keeps returning the nested office payload the UI consumes."""
    response = bare_client.get(
        f"/smardboard/side-menu/{seeded_data['office_numbers']['test_office']}"
    )
    body = json_of(response)

    assert_json_response(response, 200)
    validate_schema(body, SMARTBOARD_SIDE_MENU_RESPONSE_SCHEMA)

    office = body["office"]
    assert office["office_number"] == seeded_data["office_numbers"]["test_office"]
    assert office["timezone"]["timezone_name"] == seeded_data["office_timezones"]["test_office"]
    assert "currently_waiting" in office
