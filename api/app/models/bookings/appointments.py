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
from sqlalchemy_utc import UtcDateTime, utcnow
from sqlalchemy import func, or_, and_
from datetime import datetime, timedelta, timezone
from dateutil.parser import parse
from dateutil import tz
from app.utilities.date_util import current_pacific_time
from sqlalchemy.ext.declarative import declared_attr
from flask import g


class Appointment(Base):
    __versioned__ = {
        'exclude': []
    }

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
    online_flag = db.Column(db.Boolean(), nullable=True, default=False)
    is_draft = db.Column(db.Boolean(), nullable=True, default=False)
    created_at = db.Column(UtcDateTime, nullable=True, default=utcnow())
    stat_flag = db.Column(db.Boolean, default=False, nullable=False)
    updated_at = db.Column(UtcDateTime, onupdate=utcnow(), default=None)

    office = db.relationship("Office")
    service = db.relationship("Service")

    def __repr__(self):
        return '<Appointment ID: (name={self.appointment_id!r})>'.format(self=self)

    def __init__(self, **kwargs):
        super(Appointment, self).__init__(**kwargs)

    @declared_attr
    def updated_by(cls):  # pylint:disable=no-self-argument, # noqa: N805
        """Return updated by."""
        return db.Column('updated_by', db.String(), nullable=True, onupdate=cls._get_user_name)

    @staticmethod
    def _get_user_name(**kwargs):
        """Return current user display name."""
        _name: str = ""
        if g and 'jwt_oidc_token_info' in g:
            _name = g.jwt_oidc_token_info.get('display_name')
        return _name

    @classmethod
    def find_appointment_availability(cls, office_id: int, timezone:str, first_date: datetime, last_date: datetime):
        """Find appointment availability for dates in a month"""
        query = db.session.query(Appointment).filter(func.date_trunc('day', func.timezone(timezone, Appointment.start_time)).between(func.date_trunc('day', func.timezone(timezone, first_date)), func.date_trunc('day', func.timezone(timezone, last_date))))
        query = query.filter(Appointment.office_id == office_id)
        query = query.order_by(Appointment.start_time.asc())
        return query.all()

    @classmethod
    def find_next_day_appointments(cls):
        """Find next day appointments."""
        from app.models.theq import Office, PublicUser, Citizen, Timezone

        tomorrow = current_pacific_time() + timedelta(days=1)
        query = db.session.query(Appointment, Office, Timezone, PublicUser). \
            join(Citizen, Citizen.citizen_id == Appointment.citizen_id). \
            join(Office, Office.office_id == Appointment.office_id). \
            join(Timezone, Timezone.timezone_id == Office.timezone_id). \
            outerjoin(PublicUser, PublicUser.user_id == Citizen.user_id). \
            filter(func.date_trunc('day',
                                   func.timezone(Timezone.timezone_name, Appointment.start_time)) ==
                   tomorrow.strftime("%Y-%m-%d 00:00:00"))

        return query.all()

    @classmethod
    def get_appointment_conflicts(cls, office_id: int, start_time: str, end_time: str, appointment_id=None):
        """Find appointment availability for dates in a month"""
        from app.models.theq import Office, PublicUser, Citizen, Timezone

        start_datetime = parse(start_time)
        end_datetime = parse(end_time)
        start_time_1 = start_datetime
        end_time_1 = end_datetime - timedelta(minutes=1)

        start_time_2 = start_datetime + timedelta(minutes=1)
        end_time_2 = end_datetime

        query = db.session.query(Appointment, Office, Timezone, PublicUser). \
            join(Office, Office.office_id == Appointment.office_id). \
            join(Timezone, Timezone.timezone_id == Office.timezone_id). \
            join(Citizen, Citizen.citizen_id == Appointment.citizen_id). \
            outerjoin(PublicUser, PublicUser.user_id == Citizen.user_id). \
            filter(or_(Appointment.start_time.between(start_time_1, end_time_1), Appointment.end_time.between( start_time_2, end_time_2)))
        query = query.filter(Appointment.office_id == office_id)
        if appointment_id:
            query = query.filter(Appointment.appointment_id != appointment_id)
        return query.all()

    @classmethod
    def find_by_username_and_office_id(cls, office_id: int, user_name: str, start_time, timezone, appointment_id=None):
        """Find apponintment for the user at an office for a date."""
        from app.models.theq import PublicUser, Citizen

        start_datetime = parse(start_time)
        query = db.session.query(Appointment). \
            join(Citizen). \
            join(PublicUser). \
            filter(Appointment.citizen_id == Citizen.citizen_id). \
            filter(Citizen.user_id == PublicUser.user_id). \
            filter(func.date_trunc('day', func.timezone(timezone, Appointment.start_time)) == (func.date_trunc('day', func.timezone(timezone, start_datetime)))). \
            filter(Appointment.office_id == office_id). \
            filter(PublicUser.username == user_name). \
            filter(Appointment.checked_in_time.is_(None))
        if appointment_id:
            query = query.filter(Appointment.appointment_id != appointment_id)
        return query.all()

    @classmethod
    def delete_appointments(cls, appointment_ids: list):
        """Delete all appointments with ids in the list provided."""
        delete_qry = Appointment.__table__.delete().where(Appointment.appointment_id.in_(appointment_ids))
        db.session.execute(delete_qry)
        db.session.commit()

    @classmethod
    def find_expired_drafts(cls):
        """Find all is_draft appointments created over expiration cutoff ago."""
        EXPIRATION_CUTOFF = timedelta(minutes=15)
        expiry_limit = datetime.utcnow().replace(tzinfo=timezone.utc) - EXPIRATION_CUTOFF

        query = db.session.query(Appointment). \
            filter(Appointment.is_draft.is_(True)). \
            filter(Appointment.created_at < expiry_limit)

        return query.all()

    @classmethod
    def delete_draft(cls, draft_appointment_ids):
        """Deletes a draft appointment by id."""
        delete_qry = Appointment.__table__.delete().where(
            and_(
                Appointment.appointment_id.in_(draft_appointment_ids),
                Appointment.is_draft.is_(True)
            )
        )
        db.session.execute(delete_qry)
        db.session.commit()

    @classmethod
    def delete_expired_drafts(cls):
        """Deletes all expired drafts."""
        drafts = Appointment.find_expired_drafts()
        draft_ids = [appointment.appointment_id for appointment in drafts]
        Appointment.delete_appointments(draft_ids)
        return draft_ids
        

