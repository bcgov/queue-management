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
from sqlalchemy import func, or_
from datetime import datetime, timedelta
from dateutil.parser import parse


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
    def find_appointment_availability(cls, office_id: int, timezone:str, first_date: datetime, last_date: datetime):
        """Find appointment availability for dates in a month"""
        query = db.session.query(Appointment).filter(func.date_trunc('day', func.timezone(timezone, Appointment.start_time)).between(func.date_trunc('day', func.timezone(timezone, first_date)), func.date_trunc('day', func.timezone(timezone, last_date))))
        query = query.filter(Appointment.office_id == office_id)
        query = query.order_by(Appointment.start_time.asc())
        return query.all()

    @classmethod
    def validate_appointment_conflict(cls, office_id: int, start_time: str, end_time: str, appointment_id=None):
        """Find appointment availability for dates in a month"""
        start_datetime = parse(start_time)
        end_datetime = parse(end_time)
        start_time_1 = start_datetime
        end_time_1 = end_datetime - timedelta(minutes=1)

        start_time_2 = start_datetime + timedelta(minutes=1)
        end_time_2 = end_datetime

        query = db.session.query(Appointment).filter(or_(Appointment.start_time.between(start_time_1, end_time_1), Appointment.end_time.between( start_time_2, end_time_2)))
        query = query.filter(Appointment.office_id == office_id)
        if appointment_id:
            query = query.filter(Appointment.appointment_id != appointment_id)
        return query.all()

    @classmethod
    def find_by_citizen_id_and_office_id(cls, office_id: int, citizen_id:int, start_time, timezone, appointment_id=None):
        """Find appointment availability for dates in a month"""
        start_datetime = parse(start_time)
        query = db.session.query(Appointment). \
            filter(func.date_trunc('day', func.timezone(timezone, Appointment.start_time))==(func.date_trunc('day', func.timezone(timezone, start_datetime)))). \
            filter(Appointment.office_id == office_id). \
            filter(Appointment.citizen_id == citizen_id)
        if appointment_id:
            query = query.filter(Appointment.appointment_id != appointment_id)
        return query.all()
