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

from marshmallow import EXCLUDE
from marshmallow import fields, post_dump, pre_load

from app.models.bookings import Booking
from app.schemas import BaseSchema
from app.schemas.bookings import RoomSchema, InvigilatorSchema
from app.schemas.theq import OfficeSchema


class BookingSchema(BaseSchema):

    class Meta:
        model = Booking
        include_relationships = True
        load_instance = True
        unknown = EXCLUDE

    booking_id = fields.Int(dump_only=True)
    booking_name = fields.Str()
    end_time = fields.DateTime()
    fees = fields.Str()
    room_id = fields.Int(allow_none=True)
    start_time = fields.DateTime()
    shadow_invigilator_id = fields.Int(allow_none=True)
    office_id = fields.Int()
    sbc_staff_invigilated = fields.Int()
    booking_contact_information = fields.Str()
    blackout_flag = fields.Str(allow_none=True)
    blackout_notes = fields.Str(allow_none=True)
    recurring_uuid = fields.Str(allow_none=True)
    stat_flag = fields.Boolean(allow_none=True)

    room = fields.Nested(RoomSchema(exclude=("office",)))
    office = fields.Nested(OfficeSchema(only=('appointments_enabled_ind', 'exams_enabled_ind', 'office_id',
                                              'office_name', 'office_number', 'timezone')))

    #  NOTE:  The reason for the exclude, rather than just a single include, is because
    #         an include with a single field didn't seem to work.  When I added a second field, it worked.
    #         I only want a single field, so had to use an exclude instead.  ?????
    invigilators = fields.Nested(InvigilatorSchema(exclude=( 'contact_email', 'contract_number',
                                                            'contract_expiry_date', 'invigilator_name',
                                                            'invigilator_notes', 'shadow_count', 'shadow_flag',
                                                            'contact_phone', 'deleted', 'office'
                                                            )), many=True)

    def update_invigilators(self, data):
        invigilator_data = data.get('invigilators')
        invigilator_list = []
        #  NOTE: The not none test put in by Chris to fix an error
        #        PUT /bookings/recurring/uuid call
        if invigilator_data is not None:
            for invigilator in invigilator_data:
                identifier = invigilator.get('invigilator_id')
                invigilator_list.append(identifier)
            data['invigilators'] = invigilator_list
        return data

    @post_dump(pass_many=True)
    def fix_invigilators(self, data, many, **kwargs):
        if not many:
            data = self.update_invigilators(data)

        else:
            for booking in data:
                booking = self.update_invigilators(booking)

        return data

    @pre_load
    def convert_bool_to_int(self, in_data, **kwargs):
        if type(in_data) == dict and 'sbc_staff_invigilated' in in_data and type(
                in_data['sbc_staff_invigilated']) == bool:
            in_data['sbc_staff_invigilated'] = 1 if in_data['sbc_staff_invigilated'] else 0
        return in_data
