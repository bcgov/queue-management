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


class Appointment(Base):

    appointment_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    office_id = db.Column(db.Integer, db.ForeignKey("office.office_id"), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey("service.service_id"), nullable=False)
    start_time = db.Column(UtcDateTime, nullable=False)
    end_time = db.Column(UtcDateTime, nullable=False)
    checked_in_time = db.Column(UtcDateTime, nullable=True)
    comments = db.Column(db.String(255), nullable=True)
    citizen_name = db.Column(db.String(255), nullable=False)
    contact_information = db.Column(db.String(255), nullable=True)

    office = db.relationship("Office")
    service = db.relationship("Service")

    def __repr__(self):
        return '<Appointment ID: (name={self.appointment_id!r})>'.format(self=self)

    def __init__(self, **kwargs):
        super(Appointment, self).__init__(**kwargs)

