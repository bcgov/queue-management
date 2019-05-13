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
import toastedmarshmallow
from app.models.bookings import Appointment
from app.schemas.theq import OfficeSchema
from qsystem import ma


class AppointmentSchema(ma.ModelSchema):

    class Meta:
        model = Appointment
        jit = toastedmarshmallow.Jit

    appointment_id = fields.Int(dump_only=True)
    office_id = fields.Int()
    service_id = fields.Int()
    start_time = fields.DateTime()
    end_time = fields.DateTime()
    checked_in_time = fields.DateTime()
    comments = fields.String(allow_none=True)
    citizen_name = fields.String()
    contact_information = fields.String(allow_none=True)
