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
        'day_of_week': 'Day of week (1 for Monday and 7 for Sunday)',
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
    form_args = {
        'no_of_slots': {'default': '1'}
    }
    form_create_rules = (
        'start_time',
        'end_time',
        'day_of_week',
        'no_of_slots',
        'offices'
    )
    form_choices = {
    }

TimeslotModelView = TimeslotConfig(TimeSlot, db.session)
