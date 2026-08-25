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

from flask import has_request_context
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from qsystem import application


class Base(ModelView):
    __abstract__ = True

    def get_url(self, endpoint, **kwargs):
        new_kwargs = dict(kwargs, _external=True, _scheme=application.config['PREFERRED_URL_SCHEME'])
        return super(ModelView, self).get_url(endpoint, **new_kwargs)

    def get_current_user(self):
        if not has_request_context():
            return None

        try:
            if not current_user.is_authenticated:
                return None
        except Exception:
            return None

        return current_user

    def get_current_role_code(self):
        user = self.get_current_user()
        role = getattr(user, 'role', None)
        return getattr(role, 'role_code', None)

    def get_current_office_id(self):
        user = self.get_current_user()
        return getattr(user, 'office_id', None)
