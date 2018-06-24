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

from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
from app.models import Citizen
from qsystem import db

class CitizenSchema(ModelSchema):

    class Meta:
        model = Citizen
        sqla_session = db.session

    citizen_id          = fields.Int(dump_only=True)
    office_id           = fields.Int()
    ticket_number       = fields.Str(dump_only=True)
    citizen_name        = fields.Str()
    citizen_comments    = fields.Str()
    qt_xn_citizen_ind   = fields.Int()
    cs_id               = fields.Int()
    start_time          = fields.DateTime(dump_only=True)