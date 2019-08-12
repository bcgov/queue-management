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
from sqlalchemy_utc import UtcDateTime


class Booking(Base):

    booking_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey("room.room_id"), nullable=True)
    invigilator_id = db.Column(db.Integer, db.ForeignKey("invigilator.invigilator_id"), nullable=True)
    office_id = db.Column(db.Integer, db.ForeignKey("office.office_id"), nullable=False)
    start_time = db.Column(UtcDateTime, nullable=False)
    end_time = db.Column(UtcDateTime, nullable=False)
    fees = db.Column(db.String(5), nullable=True)
    booking_name = db.Column(db.String(150), nullable=True)
    sbc_staff_invigilated = db.Column(db.Integer, default=0)
    booking_contact_information = db.Column(db.String(256), nullable=True)
    blackout_flag = db.Column(db.String(1), default='N', nullable=False)
    blackout_notes = db.Column(db.String(255), nullable=True)

    room = db.relationship("Room")
    invigilator = db.relationship("Invigilator")
    office = db.relationship("Office")

    def __repr__(self):
        return '<Booking Name: (name={self.booking_name!r})>'.format(self=self)

    def __init__(self, **kwargs):
        super(Booking, self).__init__(**kwargs)
