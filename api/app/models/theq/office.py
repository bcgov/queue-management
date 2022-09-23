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

from qsystem import db
from app.models.theq import Base
from app.models.bookings import Exam, Room
from qsystem import cache, db
import enum
from sqlalchemy import Enum, desc


class Status(enum.Enum):
    SHOW = 'SHOW'
    HIDE = 'HIDE'
    DISABLE = 'DISABLE'


class Office(Base):
    # Defining String constants to appease SonarQube
    office_id_const = 'office.office_id'
    service_id_const = 'service.service_id'
    
    office_service = db.Table(
        'office_service',
        db.Column('office_id', db.Integer,
                db.ForeignKey(office_id_const, ondelete="CASCADE"), primary_key=True),
        db.Column('service_id', db.Integer,
                db.ForeignKey(service_id_const, ondelete="CASCADE"), primary_key=True))

    office_quick_list = db.Table(
        'office_quick_list',
        db.Column('office_id', db.Integer,
                db.ForeignKey(office_id_const, ondelete="CASCADE"), primary_key=True),
        db.Column('service_id', db.Integer,
                db.ForeignKey(service_id_const, ondelete="CASCADE"), primary_key=True))

    office_back_office_list = db.Table(
        'office_back_office_list',
        db.Column('office_id', db.Integer,
                db.ForeignKey(office_id_const, ondelete="CASCADE"), primary_key=True),
        db.Column('service_id', db.Integer,
                db.ForeignKey(service_id_const, ondelete="CASCADE"), primary_key=True))

    office_counter= db.Table(
        'office_counter',
        db.Column('office_id', db.Integer,
                db.ForeignKey(office_id_const, ondelete="CASCADE"), primary_key=True),
        db.Column('counter_id', db.Integer,
                db.ForeignKey('counter.counter_id', ondelete="CASCADE"), primary_key=True))

    office_timeslot = db.Table(
        'office_timeslot',
        db.Column('office_id', db.Integer,
                  db.ForeignKey(office_id_const, ondelete="CASCADE"), primary_key=True),
        db.Column('time_slot_id', db.Integer,
                  db.ForeignKey('timeslot.time_slot_id', ondelete="CASCADE"), primary_key=True))

    office_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    office_name = db.Column(db.String(100))
    office_number = db.Column(db.Integer)
    sb_id = db.Column(db.Integer, db.ForeignKey('smartboard.sb_id'))
    deleted = db.Column(db.DateTime, nullable=True)
    exams_enabled_ind = db.Column(db.Integer, nullable=False)
    appointments_enabled_ind = db.Column(db.Integer, nullable=False, default=0)
    timezone_id = db.Column(db.Integer, db.ForeignKey('timezone.timezone_id'), nullable=True)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    office_appointment_message = db.Column(db.String(1000))
    appointments_days_limit = db.Column(db.Integer, default=30)
    appointment_duration = db.Column(db.Integer, default=30)
    max_person_appointment_per_day = db.Column(db.Integer, default=1)
    civic_address = db.Column(db.String(200))
    telephone = db.Column(db.String(20))
    online_status = db.Column(Enum(Status))
    number_of_dlkt = db.Column(db.Integer, nullable=True)
    office_email_paragraph = db.Column(db.String(2000), nullable=True)
    external_map_link = db.Column(db.String(500), nullable=True)
    soonest_appointment = db.Column(db.Integer, default=0)

    counters = db.relationship("Counter", secondary='office_counter')
    services = db.relationship("Service", secondary='office_service')
    quick_list = db.relationship("Service", secondary='office_quick_list')
    back_office_list = db.relationship("Service", secondary='office_back_office_list')
    csrs = db.relationship('CSR')
    citizens = db.relationship('Citizen', backref='office_citizens')
    timeslots = db.relationship('TimeSlot')

    sb = db.relationship('SmartBoard')
    timezone = db.relationship('Timezone')

    exams = db.relationship("Exam")
    rooms = db.relationship('Room')

    # for walk-in notifications
    check_in_notification = db.Column(db.Integer)
    check_in_reminder_msg = db.Column(db.Text)
    automatic_reminder_at = db.Column(db.Integer)
    # for Digital Signage
    currently_waiting = db.Column(db.Integer)
    digital_signage_message = db.Column(db.Integer)
    digital_signage_message_1 = db.Column(db.Text)
    digital_signage_message_2 = db.Column(db.Text)
    digital_signage_message_3 = db.Column(db.Text)
    show_currently_waiting_bottom = db.Column(db.Integer)
    

    format_string = 'office_%s'
    offices_cache_key: str = 'active_offices'

    def __repr__(self):
        return self.office_name

    def __init__(self, **kwargs):
        super(Office, self).__init__(**kwargs)

    @classmethod
    def find_by_id(cls, office_id: int):
        """Return a Office by office_id."""
        key = Office.format_string % office_id
        office = cache.get(key)
        if not office:
            office = cls.query.get(office_id)
            office.timeslots
            office.timezone
        return office

    @classmethod
    def build_cache(cls):
        """Build cache."""
        try:
            all_offices = cls.query.all()
            for office in all_offices:
                key = Office.format_string % office.office_id
                office.timeslots
                office.timezone
                cache.set(key, office)
        except Exception:
            print('Error on building cache')

    @classmethod
    def get_all_active_offices(cls):
        """Return all active offices."""
        from app.schemas.theq import OfficeSchema

        active_offices = cache.get(Office.offices_cache_key)
        if not active_offices:
            office_schema = OfficeSchema(many=True)
            active_offices = office_schema.dump(Office.query.filter(Office.deleted.is_(None)).order_by(Office.office_name))
            cache.set(Office.offices_cache_key, active_offices)
        return active_offices

    @classmethod
    def clear_offices_cache(cls):
        """Clear active offices cache."""
        cache.delete(Office.offices_cache_key)
