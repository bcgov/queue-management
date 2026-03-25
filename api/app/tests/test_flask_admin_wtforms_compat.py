from flask_admin.contrib.sqla.fields import QuerySelectField
from flask_admin.contrib.sqla.validators import Unique
from flask_admin.form.fields import Select2Field
from flask_admin.form.validators import FieldListInputRequired
from wtforms import Form
from wtforms.fields import SelectFieldBase

from app.utilities.flask_admin_compat import apply_wtforms_compat


def test_apply_wtforms_compat_normalizes_legacy_tuple_flags():
    FieldListInputRequired.field_flags = ("required",)
    Unique.field_flags = ("unique",)

    apply_wtforms_compat()

    assert FieldListInputRequired.field_flags == {"required": True}
    assert Unique.field_flags == {"unique": True}


def test_apply_wtforms_compat_normalizes_select2_iter_choices():
    class TestForm(Form):
        status = Select2Field(choices=[("1", "Active")])

    apply_wtforms_compat()

    form = TestForm()

    assert list(form.status.iter_choices()) == [("1", "Active", False, {})]


def test_apply_wtforms_compat_normalizes_query_select_iter_choices():
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
    class LegacySelectField(SelectFieldBase):
        widget = Select2Field.widget

        def iter_choices(self):
            yield ("1", "Active", False)

    class TestForm(Form):
        status = LegacySelectField()

    apply_wtforms_compat()

    form = TestForm()

    assert 'option value="1"' in form.status()
