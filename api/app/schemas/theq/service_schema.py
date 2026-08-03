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

from marshmallow import fields
from app.models.theq import Service
from qsystem import ma
from app.schemas import BaseSchema


class ServiceSchema(BaseSchema):

    class Meta(BaseSchema.Meta):
        model = Service
        include_relationships = True
        include_fk = True

    service_id = fields.Int(dump_only=True)
    service_code = fields.Str(dump_only=True)
    service_name = fields.Str(dump_only=True)
    service_desc = fields.Str(dump_only=True)
    parent = fields.Nested('self', only=('service_name',))
    parent_id = fields.Int(dump_only=True)
    deleted = fields.DateTime(dump_only=True)
    prefix = fields.Str(dump_only=True)
    display_dashboard_ind = fields.Int(dump_only=True)
    actual_service_ind = fields.Int(dump_only=True)
    external_service_name = fields.Str(dump_only=True)
    online_link = fields.Str(dump_only=True)
    online_availability = fields.Str(dump_only=True)
    timeslot_duration = fields.Int(dump_only=True)
    email_paragraph = fields.Str(dump_only=True)
    css_colour = fields.Str(dump_only=True)
    is_dlkt = fields.Boolean()
    partner = fields.Str()
    program = fields.Str()
    recoverable = fields.Str()
