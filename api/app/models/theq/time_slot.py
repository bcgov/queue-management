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


class TimeSlot(Base):

    time_slot_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    day_of_week = db.Column(db.Integer)
    no_of_slots = db.Column(db.Integer, nullable=False)

    offices = db.relationship('Office', secondary='office_timeslot')

    format_string = 'time_slot_%s'


    def __repr__(self):
        return '<Timselot :(name={self.time_slot_id!r})>'.format(self=self)

    def __init__(self, **kwargs):
        super(TimeSlot, self).__init__(**kwargs)

    @classmethod
    def find_by_office_id(cls, office_id: int):
        return cls.query.filter(office_id==office_id).all()
