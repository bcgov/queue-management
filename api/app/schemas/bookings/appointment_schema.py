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
from app.models.bookings import Appointment
from app.schemas.theq import OfficeSchema, ServiceSchema
from qsystem import ma
from app.schemas import BaseSchema


class AppointmentSchema(BaseSchema):

    class Meta(BaseSchema.Meta):
        model = Appointment
        include_relationships = True

    appointment_id = fields.Int(dump_only=True)
    office_id = fields.Int()
    service_id = fields.Int(allow_none=True)
    citizen_id = fields.Int()
    start_time = fields.DateTime()
    end_time = fields.DateTime()
    checked_in_time = fields.DateTime()
    comments = fields.String(allow_none=True)
    citizen_name = fields.String()
    contact_information = fields.String(allow_none=True)
    blackout_flag = fields.String(allow_none=True)
    recurring_uuid = fields.String(allow_none=True)
    online_flag = fields.Boolean(allow_none=True)
    is_draft = fields.Boolean(allow_none=True)
    stat_flag = fields.Boolean(allow_none=True)
    office = fields.Nested(OfficeSchema(exclude=('sb', 'counters', 'quick_list', 'back_office_list', 'timeslots')))
    service = fields.Nested(ServiceSchema())

