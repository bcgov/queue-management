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
from app.models.theq import Office
from app.schemas.theq import SmartBoardSchema, CounterSchema, ServiceSchema, TimezoneSchema, TimeslotSchema
from qsystem import ma
from app.schemas import BaseSchema


class OfficeSchema(BaseSchema):

    class Meta(BaseSchema.Meta):
        model = Office
        include_relationships = True

    office_id = fields.Int()
    office_name = fields.Str()
    office_number = fields.Int()
    sb_id = fields.Int()
    deleted = fields.DateTime()
    exams_enabled_ind = fields.Int()
    appointments_enabled_ind = fields.Int()
    max_person_appointment_per_day = fields.Int()
    telephone = fields.Str()
    appointments_days_limit = fields.Int()
    appointment_duration = fields.Int()

    sb = fields.Nested(SmartBoardSchema())
    counters = fields.Nested(CounterSchema(), many=True)
    quick_list = fields.Nested(ServiceSchema(), many=True)
    back_office_list = fields.Nested(ServiceSchema(), many=True)
    timezone = fields.Nested(TimezoneSchema())
    timeslots = fields.Nested(TimeslotSchema(), many=True)

    latitude = fields.Float()
    longitude = fields.Float()
    office_appointment_message = fields.Str()
    civic_address = fields.Str()
    online_status = fields.Str()
    external_map_link = fields.Str()

    # for walk-in notifications
    check_in_notification = fields.Int()
    check_in_reminder_msg = fields.Str()
    automatic_reminder_at = fields.Int()

    # for Digital Signage
    currently_waiting = fields.Int()
    digital_signage_message = fields.Int()
    digital_signage_message_1 = fields.Str()
    digital_signage_message_2 = fields.Str()
    digital_signage_message_3 = fields.Str()
    show_currently_waiting_bottom = fields.Int()
