from __future__ import annotations

from dataclasses import dataclass

import pytest
from app.tests.api_test_support import (
    assert_forbidden,
    assert_status,
    assert_unauthorized,
    create_public_user,
    json_of,
    public_slot_payload,
)

pytestmark = [pytest.mark.auth, pytest.mark.usefixtures("seeded_database")]


@dataclass(frozen=True)
class PublicRouteCase:
    """Describe a public-user-only route and the request needed to reach it."""

    id: str
    method: str
    build_request: object
    expected_status: int


def _create_user_request(ctx):
    return {"path": "/users/"}


def _update_user_request(ctx):
    user = create_public_user(ctx["public_client"])
    return {
        "path": f"/users/{user['user_id']}/",
        "json": {
            "email": "updated-public@example.com",
            "telephone": "2505550100",
            "send_email_reminders": True,
            "send_sms_reminders": True,
        },
    }


def _me_request(ctx):
    create_public_user(ctx["public_client"])
    return {"path": "/users/me/"}


def _appointments_request(ctx):
    create_public_user(ctx["public_client"])
    payload, _day_key, _slots = public_slot_payload(
        ctx["public_client"], ctx["seeded_data"], minimum_slots=1
    )
    create_response = ctx["public_client"].post("/appointments/", json=payload)
    assert_status(create_response, 201)
    return {"path": "/users/appointments/"}


PUBLIC_ROUTE_CASES = [
    PublicRouteCase("POST /users/", "POST", _create_user_request, 200),
    PublicRouteCase("PUT /users/<user_id>/", "PUT", _update_user_request, 200),
    PublicRouteCase("GET /users/me/", "GET", _me_request, 200),
    PublicRouteCase("GET /users/appointments/", "GET", _appointments_request, 200),
]


def _context(bare_client, internal_ga_client, public_client, seeded_data):
    return {
        "bare_client": bare_client,
        "internal_ga_client": internal_ga_client,
        "public_client": public_client,
        "seeded_data": seeded_data,
    }


@pytest.mark.parametrize("case", PUBLIC_ROUTE_CASES, ids=lambda case: case.id)
def test_bare_client_receives_401_for_public_user_routes(
    bare_client, case, internal_ga_client, public_client, seeded_data
):
    """Assert that public-user routes still require an authenticated public identity."""
    ctx = _context(bare_client, internal_ga_client, public_client, seeded_data)
    request_kwargs = case.build_request(ctx)

    response = bare_client.open(
        request_kwargs.pop("path"), method=case.method, **request_kwargs
    )

    assert_unauthorized(response)


@pytest.mark.parametrize("case", PUBLIC_ROUTE_CASES, ids=lambda case: case.id)
def test_internal_user_receives_403_for_public_user_routes(
    bare_client, case, internal_ga_client, public_client, seeded_data
):
    """Assert that internal users remain forbidden from public-user-only routes."""
    ctx = _context(bare_client, internal_ga_client, public_client, seeded_data)
    request_kwargs = case.build_request(ctx)

    response = internal_ga_client.open(
        request_kwargs.pop("path"), method=case.method, **request_kwargs
    )

    assert_forbidden(response)


@pytest.mark.parametrize("case", PUBLIC_ROUTE_CASES, ids=lambda case: case.id)
def test_public_user_can_reach_public_user_routes(
    bare_client, case, internal_ga_client, public_client, seeded_data
):
    """Assert that authenticated public users still reach their user-management routes."""
    ctx = _context(bare_client, internal_ga_client, public_client, seeded_data)
    request_kwargs = case.build_request(ctx)

    response = public_client.open(
        request_kwargs.pop("path"), method=case.method, **request_kwargs
    )

    assert_status(response, case.expected_status)
    assert response.get_json() is not None
