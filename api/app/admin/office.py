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


from app.models.theq import Office
from .base import Base
from flask_login import current_user
from qsystem import db


class OfficeConfig(Base):
    roles_allowed = ['SUPPORT']

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role.role_code in self.roles_allowed

    create_modal = False
    edit_modal = False
    can_delete = False
    column_list = ['office_name', 'sb', 'services', 'deleted', 'exams_enabled_ind', 'timezone.timezone_name']
    form_excluded_columns = ('citizens', 'csrs', 'exams', 'rooms', 'invigilators')
    form_create_rules = ('office_name', 'office_number', 'sb', 'services', 'deleted', 'exams_enabled_ind',
                         'appointments_enabled_ind', 'timezone')
    form_edit_rules = ('office_name', 'office_number', 'sb', 'services', 'deleted', 'exams_enabled_ind',
                       'appointments_enabled_ind', 'timezone')
    column_labels = {'sb': 'Smartboard', 'timezone.timezone_name': 'Timezone Name'}
    column_sortable_list = ['office_name', 'sb', 'deleted', 'exams_enabled_ind']
    column_default_sort = 'office_name'


OfficeModelView = OfficeConfig(Office, db.session)
