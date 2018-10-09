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

from qsystem import application
from flask_admin import AdminIndexView, expose


class HomeView(AdminIndexView):

    @expose('/')
    def index(self):
        return self.render('admin/base.html')

    def get_url(self, endpoint, **kwargs):
        new_kwargs = dict(kwargs, _external=True, _scheme=application.config['PREFERRED_URL_SCHEME'])
        return super(AdminIndexView, self).get_url(endpoint, **new_kwargs)
