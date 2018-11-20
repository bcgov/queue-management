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

import toastedmarshmallow
from marshmallow import fields
from api.app.models.theq import Service
from api.app.schemas.theq import OfficeSchema
from qsystem import ma


class ServiceSchema(ma.ModelSchema):

    class Meta:
        model = Service
        jit = toastedmarshmallow.Jit
        include_fk = True
        exclude = ('offices',)

    service_id = fields.Int(dump_only=True)
    service_code = fields.Str(dump_only=True)
    service_name = fields.Str(dump_only=True)
    service_desc = fields.Str(dump_only=True)
    parent = fields.Nested('self', only=('service_name',))
    deleted = fields.DateTime(dump_only=True)
    prefix = fields.Str(dump_only=True)
    display_dashboard_ind = fields.Int(dump_only=True)
    actual_service_ind = fields.Int(dump_only=True)
