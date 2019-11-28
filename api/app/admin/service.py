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

from app.models.theq import Service
from .base import Base
from flask_login import current_user
from qsystem import db


class ServiceConfig(Base):
    roles_allowed = ['ANALYTICS', 'SUPPORT']

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role.role_code in self.roles_allowed

    create_modal = False
    edit_modal = False
    can_delete = False
    column_list = [
        'service_code',
        'service_name',
        'service_desc',
        'parent',
        'offices',
        'actual_service_ind',
        'display_dashboard_ind',
        'prefix',
        'deleted'
    ]
    column_labels = {
        'service_desc': 'Description',
        'deleted': 'Deleted',
        'display_dashboard_ind': 'Display Add Citizen/Back Office',
        'actual_service_ind': 'Category or Service'
    }
    column_searchable_list = ('service_code','service_name',)
    column_sortable_list = [
        'service_code',
        'service_name',
        'parent',
        'prefix',
        'actual_service_ind',
        'display_dashboard_ind',
        'deleted'
    ]
    column_default_sort = 'service_name'
    form_args = {
        'actual_service_ind': {'default': '1'},
        'display_dashboard_ind': {'default': '1'}
    }
    form_create_rules = (
        'service_code',
        'service_name',
        'service_desc',
        'parent',
        'offices',
        'actual_service_ind',
        'display_dashboard_ind',
        'prefix',
        'deleted',
    )
    form_choices = {
        'actual_service_ind': [
            ("0", 'This is a category'), ("1", 'This is a service')
        ],
        'display_dashboard_ind': [
            ("0", 'No, do not display in the Add Citizen service list'),\
            ("1", 'Yes, display in the Add Citizen service list')
        ]
    }

ServiceModelView = ServiceConfig(Service, db.session)
