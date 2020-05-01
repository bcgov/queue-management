'''Copyright 2018 Province of British Columbia

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.'''

from app.models.theq import TimeSlot
from .base import Base
from flask_login import current_user
from qsystem import db
import enum
from flask_admin.form.fields import Select2Field


class MultipleSelect2Field(Select2Field):
    """Extends select2 field to make it work with postgresql arrays and using choices.

    It is far from perfect and it should be tweaked it a bit more.
    """

    def iter_choices(self):
        """Iterate over choices especially to check if one of the values is selected."""
        if self.allow_blank:
            yield (u'__None', self.blank_text, self.data is None)

        for value, label in self.choices:
            yield (value, label, self.coerce(value) in self.data)

    def process_data(self, value):
        """This is called when you create the form with existing data."""
        if value is None:
            self.data = []
        else:
            try:
                self.data = [self.coerce(value) for value in value]
            except (ValueError, TypeError):
                self.data = []

    def process_formdata(self, valuelist):
        """Process posted data."""
        if not valuelist:
            return

        if valuelist[0] == '__None':
            self.data = []
        else:
            try:
                self.data = [self.coerce(value) for value in valuelist]
            except ValueError:
                raise ValueError(self.gettext(u'Invalid Choice: could not coerce'))

    def pre_validate(self, form):
        """Validate sent keys to make sure user don't post data that is not a valid choice."""
        sent_data = set(self.data)
        valid_data = {k for k, _ in self.choices}
        invalid_keys = sent_data - valid_data
        if invalid_keys:
            raise ValueError('These values are invalid {}'.format(','.join(invalid_keys)))


class TimeslotConfig(Base):
    roles_allowed = ['ANALYTICS', 'SUPPORT']

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role.role_code in self.roles_allowed

    create_modal = False
    edit_modal = False
    can_delete = False
    column_list = [
        'start_time',
        'end_time',
        'day_of_week',
        'no_of_slots',
        'offices'
    ]
    column_labels = {
        'start_time': 'Start Time (HH:MM format)',
        'end_time': 'End Time (HH:MM format)',
        'day_of_week': 'Day of week',
        'no_of_slots': 'No of appointment available per slot'
    }
    column_searchable_list = ()
    column_sortable_list = [
        'start_time',
        'end_time',
        'day_of_week',
        'no_of_slots'
    ]
    column_default_sort = 'start_time'

    choices = [
        ('Monday','Monday'),
        ('Tuesday','Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday','Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday')
    ]

    form_args = dict(day_of_week=dict(render_kw=dict(multiple="multiple"), choices=choices))

    form_overrides = {
        'day_of_week': MultipleSelect2Field
    }


    form_create_rules = (
        'start_time',
        'end_time',
        'day_of_week',
        'no_of_slots',
        'offices'
    )


TimeslotModelView = TimeslotConfig(TimeSlot, db.session)
