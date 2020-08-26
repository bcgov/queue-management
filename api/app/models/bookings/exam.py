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
    booking_id = db.Column(db.Integer, db.ForeignKey("booking.booking_id", ondelete="set null"), nullable=True)
    exam_type_id = db.Column(db.Integer, db.ForeignKey("examtype.exam_type_id"), nullable=True)
    office_id = db.Column(db.Integer, db.ForeignKey("office.office_id"), nullable=False)
    invigilator_id = db.Column(db.Integer, db.ForeignKey("invigilator.invigilator_id"), nullable=True)
    event_id = db.Column(db.String(25), nullable=True)
    exam_name = db.Column(db.String(50), nullable=False)
    examinee_name = db.Column(db.String(50), nullable=True)
    examinee_email = db.Column(db.String(400), nullable=True)
    examinee_phone = db.Column(db.String(400), nullable=True)
    expiry_date = db.Column(db.DateTime, nullable=True)
    notes = db.Column(db.String(400), nullable=True)
    exam_received_date = db.Column(db.DateTime, nullable=True)
    session_number = db.Column(db.Integer, nullable=True)
    number_of_students = db.Column(db.Integer, nullable=True)
    exam_method = db.Column(db.String(15), nullable=False)
    deleted_date = db.Column(db.String(50), nullable=True)
    exam_returned_date = db.Column(db.DateTime, nullable=True)
    exam_returned_tracking_number = db.Column(db.String(255), nullable=True)
    exam_written_ind = db.Column(db.Integer, nullable=False, default=0)
    offsite_location = db.Column(db.String(50), nullable=True)
    bcmp_job_id = db.Column(db.String(100), nullable=True)
    exam_destroyed_date = db.Column(db.String(50), nullable=True)
    upload_received_ind = db.Column(db.Integer, nullable=True, default=0)
    sbc_managed_ind = db.Column(db.Integer, nullable=True, default=0)
    receipt = db.Column(db.String(50), nullable=True)
    payee_ind = db.Column(db.Integer, nullable=True, default=0)
    receipt_sent_ind = db.Column(db.Integer, nullable=True, default=0)
    payee_email = db.Column(db.String(50), nullable=True)
    payee_name = db.Column(db.String(50), nullable=True)
    payee_phone = db.Column(db.String(50), nullable=True)
    candidates_list = db.Column(db.JSON, nullable=True)
    is_pesticide = db.Column(db.Integer, nullable=True, default=0)

    booking = db.relationship("Booking")
    exam_type = db.relationship("ExamType")
    office = db.relationship("Office")
    invigilator = db.relationship("Invigilator")

    def __repr__(self):
        return '<Exam Name: (name={self.exam_name!r})>'.format(self=self)

    def __init__(self, **kwargs):
        super(Exam, self).__init__(**kwargs)
