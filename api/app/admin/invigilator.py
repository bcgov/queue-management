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

from app.models.bookings import Invigilator
from .base import Base
from flask_login import current_user
from qsystem import db
from wtforms import validators


class InvigilatorConfig(Base):
    roles_allowed = ['SUPPORT', 'GA']

    # Defining String constants to appease SonarQube
    office_name_const = 'office.office_name'

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role.role_code in self.roles_allowed

    def get_query(self):
        if current_user.role.role_code == 'SUPPORT':
            return self.session.query(self.model)
        elif current_user.role.role_code == 'GA':
            return self.session.query(self.model).filter_by(office_id=current_user.office_id)

    create_modal = False
    edit_modal = False
    can_delete = False

    column_list = [
        office_name_const,
        'invigilator_name',
        'contact_phone',
        'contact_email',
        'contract_number',
        'contract_expiry_date',
        'invigilator_notes',
        'shadow_count',
        'shadow_flag',
        'deleted',
    ]

    form_args = {
        'shadow_count': {'default': '0'},
        'shadow_flag': {'default': 'N'}
    }

    form_excluded_columns = [
        'bookings'
    ]

    column_labels = {
        office_name_const: 'Office Name',
        'shadow_count': 'Shadow Session Count',
        'shadow_flag': 'Shadow Sessions Completed',
        'deleted': 'Deleted'
    }

    column_searchable_list = {
        'invigilator_name',
        'shadow_count',
        'shadow_flag',
        'deleted',
        office_name_const
    }

    form_create_rules = (
        'office',
        'invigilator_name',
        'contact_phone',
        'contact_email',
        'contract_number',
        'contract_expiry_date',
        'invigilator_notes',
        'shadow_count',
        'shadow_flag',
        'deleted'
    )

    form_choices = {
        'shadow_count': [
            ('0', '0'),
            ('1', '1'),
            ('2', '2')
        ],
        'shadow_flag': [
            ('N', 'No'),
            ('Y', 'Yes')
        ]
    }

    form_edit_rules = (
        'office',
        'invigilator_name',
        'contact_phone',
        'contact_email',
        'contract_number',
        'contract_expiry_date',
        'invigilator_notes',
        'shadow_count',
        'shadow_flag',
        'deleted',
    )

    column_sortable_list = [
        'invigilator_name',
        'contact_email',
        'contract_number',
        'contract_expiry_date',
        'shadow_count',
        'shadow_flag',
        'deleted',
    ]

    column_default_sort = 'invigilator_name'

    def on_model_change(self, form, model, is_created):

        shadow_count = int(model.shadow_count)
        shadow_flag = model.shadow_flag

        if shadow_count < 0 or shadow_count > 2:
            raise validators.ValidationError('Invigilator Shadow Count is outside of set range.')
        if shadow_flag == 'Y' and shadow_count < 2:
            raise validators.ValidationError('Invigilator Shadow Sessions Completed is set to YES with a Shadow '
                                             'Session Count less than 2.')


InvigilatorModelView = InvigilatorConfig(Invigilator, db.session)
