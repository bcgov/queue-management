"""Compatibility helpers for Flask-Admin on newer WTForms releases."""

from collections.abc import Mapping

from flask_admin._backwards import Markup
from flask_admin.contrib.sqla.fields import QuerySelectField, QuerySelectMultipleField
from flask_admin.contrib.sqla.widgets import CheckboxListInput
from flask_admin.contrib.sqla.validators import Unique
from flask_admin.form.fields import Select2Field
from flask_admin.form.validators import FieldListInputRequired
from wtforms.widgets.core import Select, escape, html_params


def _normalize_field_flags(validator_class):
    """WTForms 3.2 expects validator field_flags to be a mapping."""
    field_flags = getattr(validator_class, "field_flags", {})
    if isinstance(field_flags, Mapping):
        return

    validator_class.field_flags = {flag: True for flag in field_flags}


def _normalize_iter_choices(field_class):
    """WTForms 3.2 expects select choices to include render_kw."""
    if getattr(field_class, "_wtforms_compat_choices_patched", False):
        return

    original_iter_choices = field_class.iter_choices

    def wrapped_iter_choices(self):
        for choice in original_iter_choices(self):
            yield _normalize_choice(choice)

    field_class.iter_choices = wrapped_iter_choices
    field_class._wtforms_compat_choices_patched = True


def _normalize_choice(choice):
    if len(choice) == 3:
        return (*choice, {})
    return choice


def _patch_select_widget():
    if getattr(Select, "_wtforms_compat_choices_patched", False):
        return

    def wrapped_call(self, field, **kwargs):
        kwargs.setdefault("id", field.id)
        if self.multiple:
            kwargs["multiple"] = True

        flags = getattr(field, "flags", {})
        for key in dir(flags):
            if key in self.validation_attrs and key not in kwargs:
                kwargs[key] = getattr(flags, key)

        select_params = html_params(name=field.name, **kwargs)
        html = [f"<select {select_params}>"]

        if field.has_groups():
            for group, choices in field.iter_groups():
                optgroup_params = html_params(label=group)
                html.append(f"<optgroup {optgroup_params}>")
                for choice in choices:
                    value, label, selected, render_kw = _normalize_choice(choice)
                    html.append(self.render_option(value, label, selected, **render_kw))
                html.append("</optgroup>")
        else:
            for choice in field.iter_choices():
                value, label, selected, render_kw = _normalize_choice(choice)
                html.append(self.render_option(value, label, selected, **render_kw))

        html.append("</select>")
        return Markup("".join(html))

    Select.__call__ = wrapped_call
    Select._wtforms_compat_choices_patched = True


def _patch_checkbox_list_widget():
    if getattr(CheckboxListInput, "_wtforms_compat_choices_patched", False):
        return

    def wrapped_call(self, field, **kwargs):
        items = []
        for choice in field.iter_choices():
            value, label, selected, _render_kw = _normalize_choice(choice)
            args = {
                "id": value,
                "name": field.name,
                "label": escape(label),
                "selected": " checked" if selected else "",
            }
            items.append(self.template % args)
        return Markup("".join(items))

    CheckboxListInput.__call__ = wrapped_call
    CheckboxListInput._wtforms_compat_choices_patched = True


def apply_wtforms_compat():
    """Patch known Flask-Admin validators that still use legacy tuple flags."""
    for validator_class in (FieldListInputRequired, Unique):
        _normalize_field_flags(validator_class)

    for field_class in (Select2Field, QuerySelectField, QuerySelectMultipleField):
        _normalize_iter_choices(field_class)

    _patch_select_widget()
    _patch_checkbox_list_widget()
