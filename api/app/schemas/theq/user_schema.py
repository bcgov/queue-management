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
from app.models.theq import PublicUser
from app.schemas.theq import ServiceReqSchema, CitizenStateSchema, OfficeSchema
from qsystem import ma
from app.schemas import BaseSchema


class UserSchema(BaseSchema):

    class Meta(BaseSchema.Meta):
        model = PublicUser
        include_relationships = True

    telephone = fields.String()
    send_email_reminders = fields.Boolean()
    email = fields.String()
    display_name = fields.String()
    last_name = fields.String()
    username = fields.String()
    user_id = fields.Int(dump_only=True)
    send_sms_reminders = fields.Boolean()

    # appointment_id = fields.Int(dump_only=True)
    # office_id = fields.Int()
    # service_id = fields.Int(allow_none=True)
    # citizen_id = fields.Int()
    # start_time = fields.DateTime()
    # end_time = fields.DateTime()
    # checked_in_time = fields.DateTime()
    # comments = fields.String(allow_none=True)
    # citizen_name = fields.String()
    # contact_information = fields.String(allow_none=True)
    # blackout_flag = fields.String(allow_none=True)
    # recurring_uuid = fields.String(allow_none=True)
    # online_flag = fields.Boolean(allow_none=True)
    # office = fields.Int(attribute="office_id")
