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

from app.models.theq import Role
from .base import Base
from flask_login import current_user
from qsystem import db


class RoleConfig(Base):
    roles_allowed = ['SUPPORT']

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role.role_code in self.roles_allowed

    create_modal = False
    edit_modal = False
    form_excluded_columns = ('roles',)
    column_labels = {'role_desc': 'Role Description'}
    form_create_rules = ('role_code', 'role_desc')
    form_edit_rules = ('role_code', 'role_desc')


RoleModelView = RoleConfig(Role, db.session)
