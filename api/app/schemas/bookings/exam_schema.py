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
from app.models.bookings import Exam
from app.schemas.bookings import BookingSchema, ExamTypeSchema, InvigilatorSchema
from app.schemas.theq import OfficeSchema
from qsystem import ma


class CandidateSchema(ma.SQLAlchemySchema):
    examinee_name = fields.String()
    examinee_email = fields.String()
    exam_type_id = fields.String()
    fees = fields.String()
    payee_ind = fields.String()
    receipt = fields.String()
    receipt_number = fields.String()
    payee_name = fields.String()
    payee_email = fields.String()


class ExamSchema(ma.SQLAlchemySchema):

    class Meta:
        model = Exam
        include_relationships = True
        load_instance = True
        jit = toastedmarshmallow.Jit

    booking_id = fields.Int()
    deleted_date = fields.Str()
    event_id = fields.Str()
    exam_destroyed_date = fields.Str()
    exam_id = fields.Int(dump_only=True)
    exam_method = fields.Str()
    exam_name = fields.Str()
    exam_received = fields.Int()
    exam_received_date = fields.DateTime(allow_none=True)
    exam_type_id = fields.Int()
    examinee_name = fields.Str()
    examinee_phone = fields.Str()
    examinee_email = fields.Str()
    expiry_date = fields.DateTime()
    notes = fields.Str(allow_none=True)
    number_of_students = fields.Int()
    office_id = fields.Int()
    invigilator_id = fields.Int()
    session_number = fields.Int()
    exam_returned_ind = fields.Int()
    exam_returned_date = fields.Str(allow_none=True)
    exam_returned_tracking_number = fields.Str(allow_none=True)
    exam_written_ind = fields.Int()
    upload_received_ind = fields.Int()
    offsite_location = fields.Str()
    sbc_managed_ind = fields.Int()
    receipt = fields.Str()
    receipt_number = fields.Str()
    fees = fields.Str()
    payee_ind = fields.Int()
    receipt_sent_ind = fields.Int()
    payee_name = fields.Str()
    payee_email = fields.Str()
    payee_phone = fields.Str()
    bcmp_job_id = fields.Str(allow_none=True)
    is_pesticide = fields.Int(allow_none=True)
    candidates_list = fields.Nested(CandidateSchema)

    booking = fields.Nested(BookingSchema())
    exam_type = fields.Nested(ExamTypeSchema())
    invigilator = fields.Nested(InvigilatorSchema())
    office = fields.Nested(OfficeSchema(only=('appointments_enabled_ind', 'exams_enabled_ind', 'office_id',
                                              'office_name', 'office_number', 'timezone')))

