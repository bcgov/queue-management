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


from app.models import CSR
from flask_admin.contrib.sqla import ModelView
from qsystem import db


class CSRConfig(ModelView):
    create_modal = True
    edit_modal = True
    can_delete = False
    column_list = ['username', 'office.office_name', 'role.role_desc', 'deleted']
    column_labels = {
        'username': 'Username',
        'office.office_name': 'Office',
        'role.role_desc': 'Role',
        'deleted': 'Deleted'
    }
    column_sortable_list = ('username', 'office.office_name', 'role.role_desc', 'deleted')
    column_default_sort = 'username'
    form_args = {
        'qt_xn_csr_ind': {'default': '0'},
        'receptionist_ind': {'default': '0'},
        'csr_state': {'default': 'Logout'}
    }
    form_excluded_columns = ('periods',)
    form_create_rules = ('username', 'qt_xn_csr_ind', 'receptionist_ind', 'csr_state', 'role', 'office','deleted',)
    form_edit_rules = ('username', 'qt_xn_csr_ind', 'receptionist_ind', 'csr_state', 'role', 'office', 'deleted',)


CSRModelView = CSRConfig(CSR, db.session)
