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
from app.models import Citizen
from app.schemas import ServiceReqSchema, CitizenStateSchema, OfficeSchema
from qsystem import ma


class CitizenSchema(ma.ModelSchema):

    class Meta:
        model = Citizen
        jit = toastedmarshmallow.Jit
        exclude = ('office_citizens','office',)

    citizen_id = fields.Int(dump_only=True)
    office_id = fields.Int()
    ticket_number = fields.Str(dump_only=True)
    citizen_comments = fields.Str()
    qt_xn_citizen_ind = fields.Int()
    start_time = fields.DateTime(dump_only=True)
    accurate_time_ind = fields.Int()
    service_reqs = fields.Nested(ServiceReqSchema(exclude=('citizen',)), many=True)
    cs = fields.Nested(CitizenStateSchema(exclude=('cs_state_desc', 'cs_id', 'citizens', 'state_citizens')))
    priority = fields.Int()
