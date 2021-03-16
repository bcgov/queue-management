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

from sqlalchemy import String
from sqlalchemy.dialects import postgresql

from app.models.theq import Base
from qsystem import db


class TimeSlot(Base):
    time_slot_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    office_id = db.Column(db.Integer, db.ForeignKey('office.office_id'), nullable=True)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    day_of_week = db.Column(postgresql.ARRAY(String), nullable=False)
    no_of_slots = db.Column(db.Integer, nullable=False)

    office = db.relationship("Office", lazy='joined')

    format_string = 'time_slot_%s'

    def __repr__(self):
        return '<Timselot :(start_time={self.start_time!r}, end_time={self.end_time!r}, day_of_week={self.day_of_week!r})>'.format(
            self=self)

    def __init__(self, **kwargs):
        super(TimeSlot, self).__init__(**kwargs)
