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


class InvigilatorConfig(Base):
    roles_allowed = ['SUPPORT', 'LIAISON']

    @property
    def can_create(self):
        return current_user.role.role_code != 'GA'

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role.role_code in self.roles_allowed

    def get_query(self):
        return self.session.query(self.model).filter_by(office_id=current_user.office_id)

    create_modal = False
    edit_modal = False
    column_list = [
        'office.office_name',
        'invigilator_name',
        'contact_phone',
        'contact_email',
        'contract_number',
        'contract_expiry_date',
        'invigilator_notes'
    ]

    form_excluded_columns = [
        'bookings'
    ]

    column_labels = {'office.office_name': 'Office Name'}

    column_searchable_list = {'invigilator_name'}

    form_create_rules = (
        'office',
        'invigilator_name',
        'contact_phone',
        'contact_email',
        'contract_number',
        'contract_expiry_date',
        'invigilator_notes'
    )

    form_edit_rules = (
        'office',
        'invigilator_name',
        'contact_phone',
        'contact_email',
        'contract_number',
        'contract_expiry_date',
        'invigilator_notes'
    )

    column_sortable_list = [
        'invigilator_name',
        'contact_email',
        'contract_number',
        'contract_expiry_date'
    ]

    column_default_sort = 'invigilator_name'


InvigilatorModelView = InvigilatorConfig(Invigilator, db.session)
