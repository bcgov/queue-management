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
    exam_type_id = fields.Int()
    examinee_name = fields.Str()
    expiry_date = fields.DateTime()
    invigilator_id = fields.Int()
    notes = fields.Str()
    number_of_students = fields.Int()
    office_id = fields.Int()
    room_id = fields.Int()
    session_number = fields.Int()

    booking = fields.Nested(BookingSchema())
    exam_type = fields.Nested(ExamTypeSchema())
    invigilator = fields.Nested(InvigilatorSchema())
    office = fields.Nested(OfficeSchema(exclude=("csrs",)))
