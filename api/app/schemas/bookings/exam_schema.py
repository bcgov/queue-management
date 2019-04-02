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
from app.schemas.bookings import BookingSchema, ExamTypeSchema
from app.schemas.theq import OfficeSchema
from qsystem import ma


class ExamSchema(ma.ModelSchema):

    class Meta:
        model = Exam
        jit = toastedmarshmallow.Jit

    booking_id = fields.Int()
    deleted_date = fields.Str()
    event_id = fields.Str()
    exam_id = fields.Int(dump_only=True)
    exam_method = fields.Str()
    exam_name = fields.Str()
    exam_received = fields.Int()
    exam_received_date = fields.DateTime(allow_none=True)
    exam_type_id = fields.Int()
    examinee_name = fields.Str()
    expiry_date = fields.DateTime()
    notes = fields.Str(allow_none=True)
    number_of_students = fields.Int()
    office_id = fields.Int()
    session_number = fields.Int()
    exam_returned_date = fields.Str(allow_none=True)
    exam_returned_tracking_number = fields.String(allow_none=True)
    exam_written_ind = fields.Int()
    offsite_location = fields.String()

    booking = fields.Nested(BookingSchema())
    exam_type = fields.Nested(ExamTypeSchema())
    office = fields.Nested(OfficeSchema(exclude=("csrs",)))
