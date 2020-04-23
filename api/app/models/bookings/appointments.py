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
from sqlalchemy import func
from datetime import datetime


class Appointment(Base):
    appointment_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    office_id = db.Column(db.Integer, db.ForeignKey("office.office_id"), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey("service.service_id"), nullable=True)
    citizen_id = db.Column(db.Integer, db.ForeignKey("citizen.citizen_id"), nullable=True)
    start_time = db.Column(UtcDateTime, nullable=False)
    end_time = db.Column(UtcDateTime, nullable=False)
    checked_in_time = db.Column(UtcDateTime, nullable=True)
    comments = db.Column(db.String(255), nullable=True)
    citizen_name = db.Column(db.String(255), nullable=False)
    contact_information = db.Column(db.String(255), nullable=True)
    blackout_flag = db.Column(db.String(1), default='N', nullable=False)
    recurring_uuid = db.Column(db.String(255), nullable=True)

    office = db.relationship("Office")
    service = db.relationship("Service")

    def __repr__(self):
        return '<Appointment ID: (name={self.appointment_id!r})>'.format(self=self)

    def __init__(self, **kwargs):
        super(Appointment, self).__init__(**kwargs)

    @classmethod
    def find_appointment_availability(cls, office_id: int, first_date: datetime, last_date: datetime):
        """Find appointment availability for dates in a month"""
        query = db.session.query(Appointment).filter(func.date_trunc('day', func.timezone('PST', Appointment.start_time)).between(first_date, last_date))
        query = query.filter(Appointment.office_id == office_id)
        query = query.order_by(Appointment.start_time.asc())
        return query.all()
        #
        # query = db.session.query(
        #     func.date_trunc('day', func.timezone('PST', Appointment.start_time)).label('day'),
        #     func.count(func.timezone('PST', Appointment.start_time)).label('no_of_appointments')
        # )
        # return query.group_by(
        #     func.date_trunc('day', func.timezone('PST', Appointment.start_time))
        # ).all()


