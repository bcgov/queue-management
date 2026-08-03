import inspect
from types import SimpleNamespace

import pytest
from app.utilities.flask_admin_compat import apply_wtforms_compat
from flask_admin.contrib.sqla.fields import QuerySelectField
from flask_admin.contrib.sqla.validators import Unique
from flask_admin.form.fields import Select2Field
from flask_admin.form.validators import FieldListInputRequired
from wtforms import Form
from wtforms.fields import SelectFieldBase


def _unwrap(func):
    return inspect.unwrap(func)


def test_application_url_map_contains_admin_and_healthz(app):
    """Assert that the Flask 3 app still exposes the admin and health routes."""
    routes = {rule.rule for rule in app.url_map.iter_rules()}

    assert "/admin/" in routes
    assert "/api/v1/healthz/" in routes


def test_admin_index_renders_without_bootstrap3_assets(client):
    """Assert that the admin index renders without legacy Bootstrap 3 assets."""
    response = client.get("/admin/")

    assert response.status_code == 200

    body = response.get_data(as_text=True)

    assert "Admin Console" in body
    assert "bootstrap3" not in body


def test_login_resource_redirects_authenticated_users_to_admin(app, monkeypatch):
    """Assert that authenticated login requests still redirect to the admin console."""
    from app.resources.theq import login as login_module

    fake_csr = SimpleNamespace(username="tester")
    logged_in = []

    monkeypatch.setattr(login_module, "get_username", lambda: "tester@idir")
    monkeypatch.setattr(login_module.CSR, "find_by_username", lambda username: fake_csr)
    monkeypatch.setattr(login_module, "login_user", lambda user: logged_in.append(user))

    handler = _unwrap(login_module.Login.get)

    with app.test_request_context("/api/v1/login/"):
        response = handler(login_module.Login())

    assert logged_in == [fake_csr]
    assert response.status_code == 302
    assert response.location.endswith("/admin/")


def test_apply_wtforms_compat_normalizes_legacy_tuple_flags():
    """Assert that legacy tuple-style field flags are normalized for WTForms 3."""
    FieldListInputRequired.field_flags = ("required",)
    Unique.field_flags = ("unique",)

    apply_wtforms_compat()

    assert FieldListInputRequired.field_flags == {"required": True}
    assert Unique.field_flags == {"unique": True}


def test_apply_wtforms_compat_normalizes_select2_iter_choices():
    """Assert that Select2 fields yield WTForms 3-compatible choice tuples."""

    class TestForm(Form):
        status = Select2Field(choices=[("1", "Active")])

    apply_wtforms_compat()

    form = TestForm()

    assert list(form.status.iter_choices()) == [("1", "Active", False, {})]


def test_apply_wtforms_compat_normalizes_query_select_iter_choices():
    """Assert that query-backed select fields yield WTForms 3-compatible choice tuples."""

    class Choice:
        def __init__(self, identifier, label):
            self.identifier = identifier
            self.label = label

    class TestForm(Form):
        role = QuerySelectField(
            query_factory=lambda: [Choice(1, "CSR")],
            get_pk=lambda obj: obj.identifier,
            get_label=lambda obj: obj.label,
        )

    apply_wtforms_compat()

    form = TestForm()

    assert list(form.role.iter_choices()) == [("1", "CSR", False, {})]


def test_apply_wtforms_compat_allows_legacy_select_widgets_to_render():
    """Assert that legacy select widgets still render after the compatibility patch is applied."""

    class LegacySelectField(SelectFieldBase):
        widget = Select2Field.widget

        def iter_choices(self):
            yield ("1", "Active", False)

    class TestForm(Form):
        status = LegacySelectField()

    apply_wtforms_compat()

    form = TestForm()

    assert 'option value="1"' in form.status()
