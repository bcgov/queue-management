from __future__ import annotations

from dataclasses import dataclass

import pytest
from app.tests.api_test_support import (
    assert_not_auth_error,
    assert_status,
    assert_unauthorized,
)
from app.tests.auth.auth_support import (
    build_bcmp_exam_payload,
    create_internal_exam_bundle,
    patch_exam_integrations,
)

pytestmark = [pytest.mark.auth, pytest.mark.usefixtures("seeded_database")]


@dataclass(frozen=True)
class AuthenticatedRouteCase:
    """Describe a route that requires authentication but uses additional in-method checks."""

    id: str
    method: str
    build_request: object
    success_assertion: object
    public_forbidden: bool = False


def _assert_exact_status(expected_status: int):
    def assertion(response):
        assert_status(response, expected_status)

    return assertion


def _build_csr_states_request(ctx):
    return {"path": "/csr_states/"}


def _build_citizens_request(ctx):
    return {"path": "/citizens/"}


def _build_invigilators_offsite_request(ctx):
    return {"path": "/invigilators/offsite/"}


def _build_exam_bcmp_request(ctx):
    patch_exam_integrations(ctx["monkeypatch"])
    return {"path": "/exams/bcmp/", "json": build_bcmp_exam_payload(ctx["seeded_data"])}


def _build_exam_bcmp_status_request(ctx):
    patch_exam_integrations(ctx["monkeypatch"])
    return {"path": "/exams/bcmp_status/", "json": {}}


def _build_exam_upload_request(ctx):
    patch_exam_integrations(ctx["monkeypatch"])
    _booking, exam = create_internal_exam_bundle(
        ctx["internal_ga_client"], ctx["seeded_data"]
    )
    return {"path": f"/exams/{exam['exam_id']}/upload/"}


def _build_exam_transfer_request(ctx):
    patch_exam_integrations(ctx["monkeypatch"])
    _booking, exam = create_internal_exam_bundle(
        ctx["internal_ga_client"], ctx["seeded_data"]
    )
    return {"path": f"/exams/{exam['exam_id']}/transfer/"}


def _build_exam_email_invigilator_request(ctx):
    patch_exam_integrations(ctx["monkeypatch"])
    _booking, exam = create_internal_exam_bundle(
        ctx["internal_ga_client"], ctx["seeded_data"]
    )
    return {
        "path": f"/exams/{exam['exam_id']}/email_invigilator/",
        "json": {
            "invigilator_id": ctx["seeded_data"]["invigilator_ids"][0],
            "invigilator_name": "Homer Simpson",
            "invigilator_email": "homer@example.com",
            "invigilator_phone": "2505550100",
        },
    }


def _build_exam_download_request(ctx):
    patch_exam_integrations(ctx["monkeypatch"])
    _booking, exam = create_internal_exam_bundle(
        ctx["internal_ga_client"], ctx["seeded_data"]
    )
    return {"path": f"/exams/{exam['exam_id']}/download/"}


AUTHENTICATED_ONLY_CASES = [
    AuthenticatedRouteCase(
        "GET /csr_states/",
        "GET",
        _build_csr_states_request,
        _assert_exact_status(200),
        public_forbidden=True,
    ),
    AuthenticatedRouteCase(
        "GET /citizens/",
        "GET",
        _build_citizens_request,
        _assert_exact_status(200),
        public_forbidden=True,
    ),
    AuthenticatedRouteCase(
        "GET /invigilators/offsite/",
        "GET",
        _build_invigilators_offsite_request,
        _assert_exact_status(200),
    ),
    AuthenticatedRouteCase(
        "POST /exams/bcmp/", "POST", _build_exam_bcmp_request, assert_not_auth_error
    ),
    AuthenticatedRouteCase(
        "POST /exams/bcmp_status/",
        "POST",
        _build_exam_bcmp_status_request,
        _assert_exact_status(200),
    ),
    AuthenticatedRouteCase(
        "GET /exams/<exam_id>/upload/",
        "GET",
        _build_exam_upload_request,
        _assert_exact_status(200),
    ),
    AuthenticatedRouteCase(
        "POST /exams/<exam_id>/transfer/",
        "POST",
        _build_exam_transfer_request,
        _assert_exact_status(202),
    ),
    AuthenticatedRouteCase(
        "POST /exams/<exam_id>/email_invigilator/",
        "POST",
        _build_exam_email_invigilator_request,
        _assert_exact_status(200),
    ),
    AuthenticatedRouteCase(
        "GET /exams/<exam_id>/download/",
        "GET",
        _build_exam_download_request,
        _assert_exact_status(200),
    ),
]


def _context(internal_ga_client, monkeypatch, public_client, seeded_data):
    return {
        "internal_ga_client": internal_ga_client,
        "monkeypatch": monkeypatch,
        "public_client": public_client,
        "seeded_data": seeded_data,
    }


@pytest.mark.parametrize("case", AUTHENTICATED_ONLY_CASES, ids=lambda case: case.id)
def test_bare_client_receives_401_for_authenticated_only_routes(
    bare_client, case, internal_ga_client, monkeypatch, public_client, seeded_data
):
    """Assert that authenticated-only routes reject missing identities before any in-method checks run."""
    ctx = _context(internal_ga_client, monkeypatch, public_client, seeded_data)
    request_kwargs = case.build_request(ctx)

    response = bare_client.open(
        request_kwargs.pop("path"), method=case.method, **request_kwargs
    )

    assert_unauthorized(response)


@pytest.mark.parametrize("case", AUTHENTICATED_ONLY_CASES, ids=lambda case: case.id)
def test_internal_user_reaches_non_auth_behavior_for_authenticated_only_routes(
    bare_client, case, internal_ga_client, monkeypatch, public_client, seeded_data
):
    """Assert that authenticated internal users still reach the non-auth behavior for authenticated-only routes."""
    ctx = _context(internal_ga_client, monkeypatch, public_client, seeded_data)
    request_kwargs = case.build_request(ctx)

    response = internal_ga_client.open(
        request_kwargs.pop("path"), method=case.method, **request_kwargs
    )

    case.success_assertion(response)


@pytest.mark.parametrize(
    "case",
    [case for case in AUTHENTICATED_ONLY_CASES if case.public_forbidden],
    ids=lambda case: case.id,
)
def test_public_user_receives_403_when_authenticated_only_routes_perform_explicit_role_checks(
    bare_client, case, internal_ga_client, monkeypatch, public_client, seeded_data
):
    """Assert that public users receive 403 only on authenticated-only routes that explicitly enforce internal roles."""
    ctx = _context(internal_ga_client, monkeypatch, public_client, seeded_data)
    request_kwargs = case.build_request(ctx)

    response = public_client.open(
        request_kwargs.pop("path"), method=case.method, **request_kwargs
    )

    assert_status(response, 403)
