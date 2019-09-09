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


from app.models.theq import Office, Service
from .base import Base
from flask_login import current_user
from flask import flash
from flask_admin.babel import gettext
from qsystem import db
from sqlalchemy import and_

class OfficeConfig(Base):
    roles_allowed = ['SUPPORT', 'GA']

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role.role_code in self.roles_allowed

    @property
    def can_create(self):
        return current_user.role.role_code != 'GA'

    def get_query(self):
        if current_user.role.role_code == 'SUPPORT':
            return self.session.query(self.model)
        elif current_user.role.role_code == 'GA':
            return self.session.query(self.model).filter_by(office_id=current_user.office_id)

    create_modal = False
    edit_modal = False
    can_delete = False
    form_create_rules = ('office_name', 'office_number', 'sb', 'services', 'deleted', 'exams_enabled_ind',
                         'appointments_enabled_ind', 'timezone')
    form_edit_rules = ('office_name', 'office_number', 'sb', 'services', 'deleted', 'exams_enabled_ind',
                       'appointments_enabled_ind', 'timezone')
    column_labels = {'sb': 'Smartboard', 'timezone.timezone_name': 'Timezone Name'}
    column_searchable_list = ('office_name',)
    column_sortable_list = ['office_name', 'sb', 'deleted', 'exams_enabled_ind']
    column_list = ['office_name',
                   'sb',
                   'services',
                   'deleted',
                   'exams_enabled_ind',
                   'appointments_enabled_ind',
                   'counters',
                   'timezone.timezone_name',
                   ]

    form_excluded_columns = ('citizens',
                             'csrs',
                             'exams',
                             'rooms',
                             'invigilators'
                             )

    form_create_rules = ('office_name',
                         'office_number',
                         'sb',
                         'services',
                         'deleted',
                         'exams_enabled_ind',
                         'appointments_enabled_ind',
                         'counters',
                         'quick_list',
                         'back_office_list',
                         'timezone',
                         )

    form_edit_rules = ('office_name',
                       'office_number',
                       'sb',
                       'services',
                       'deleted',
                       'exams_enabled_ind',
                       'appointments_enabled_ind',
                       'counters',
                       'quick_list',
                       'back_office_list',
                       'timezone'
                       )

    form_args = {
        'quick_list': {
            'query_factory': lambda: db.session.query(Service) \
                                               .filter(and_(Service.parent_id.isnot(None)), \
                                                            Service.display_dashboard_ind == 1)
        },
        'back_office_list': {
            'query_factory': lambda: db.session.query(Service) \
                                               .filter(and_(Service.parent_id.isnot(None)), \
                                                            Service.display_dashboard_ind == 0)
        }
    }


    column_labels = {'sb': 'Smartboard',
                     'timezone.timezone_name': 'Timezone Name',
                     'exams_enabled_ind': 'Exams Enabled',
                     'appointments_enabled_ind': 'Appointments Enabled',
                     }

    column_sortable_list = ['office_name',
                            'sb',
                            'deleted',
                            'exams_enabled_ind',
                            'exams_enabled_ind',
                            'appointments_enabled_ind',
                             'counters',
                            'quick_list',
                            'back_office_list',
                            ]

    column_default_sort = 'office_name'

    def on_model_change(self, form, model, is_created):
        invalid = []
        for service in model.quick_list:
            if service not in model.services:
                invalid.append(str(service))
                model.quick_list.remove(service)
        if len(invalid) != 0:
            message = ", ".join(invalid)
            flash(gettext("Services saved minus services not offered at this office: " + message), 'warning')

class OfficeConfigGA(OfficeConfig):

    #  Change what GA sees on the Office List view.
    column_labels = {'quick_list': 'Quick List', 'back_office_list': 'Back Office List'}
    column_list =   ['office_name',
                     'quick_list',
                     'back_office_list'
                    ]


    #  Change what GAs are allowed to do from what SUPPORT can do.
    form_edit_rules = ('office_name',
                       'quick_list',
                       'back_office_list'
                       )
    form_excluded_columns = ('citizens',
                             'csrs',
                             'exams',
                             'rooms',
                             'invigilators',
                             'office_number',
                             'sb',
                             'services',
                             'deleted',
                             'exams_enabled_ind',
                             'counters',
                             'timezone'
                             )
    form_widget_args = {
        'office_name': {
            'readonly': True
        }
    }

OfficeModelView = OfficeConfig(Office, db.session)
OfficeGAModelView = OfficeConfigGA(Office, db.session, endpoint='officega')
