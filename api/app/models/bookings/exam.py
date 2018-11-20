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

from app.models.bookings import Base
from qsystem import db


class Exam(Base):

    exam_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    booking_id = db.Column(db.Integer, db.ForeignKey("booking.booking_id"), nullable=True)
    exam_type_id = db.Column(db.Integer, db.ForeignKey("examtype.exam_type_id"), nullable=False)
    invigilator_id = db.Column(db.Integer, db.ForeignKey("invigilator.invigilator_id"), nullable=False)
    office_id = db.Column(db.Integer, db.ForeignKey("office.office_id"), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey("room.room_id"), nullable=False)
    event_id = db.Column(db.String(25), nullable=False)
    exam_name = db.Column(db.String(50), nullable=False)
    examinee_name = db.Column(db.String(50), nullable=False)
    expiry_date = db.Column(db.DateTime, nullable=False)
    notes = db.Column(db.String(400), nullable=True)
    exam_received = db.Column(db.Integer, nullable=False)
    session_number = db.Column(db.Integer, nullable=False)
    number_of_students = db.Column(db.Integer, nullable=False)
    exam_method = db.Column(db.String(15), nullable=False)
    deleted_date = db.Column(db.String(50), nullable=True)

    booking = db.relationship("Booking")
    exam_type = db.relationship("ExamType")
    invigilator = db.relationship("Invigilator")

    def __repr__(self):
        return '<Exam Name: (name={self.exam_name!r})>'.format(self=self)

    def __init__(self, **kwargs):
        super(Exam, self).__init__(**kwargs)
