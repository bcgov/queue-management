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


from app.models import Role
from flask_admin.contrib.sqla import ModelView
from qsystem import db


class RoleConfig(ModelView):
    create_modal = True
    edit_modal = True
    form_excluded_columns = ('roles',)
    column_labels = {'role_desc': 'Role Description'}
    form_create_rules = ('role_code', 'role_desc')
    form_edit_rules = ('role_code', 'role_desc')


RoleModelView = RoleConfig(Role, db.session)
