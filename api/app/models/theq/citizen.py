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
from api.app.models.theq import Base


class Citizen(Base):

    citizen_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    office_id = db.Column(db.Integer, db.ForeignKey('office.office_id'), nullable=False)
    ticket_number = db.Column(db.String(50), nullable=True)
    citizen_name = db.Column(db.String(150), nullable=True)
    citizen_comments = db.Column(db.String(1000), nullable=True)
    qt_xn_citizen_ind = db.Column(db.Integer, default=0, nullable=False)
    cs_id = db.Column(db.Integer, db.ForeignKey('citizenstate.cs_id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    accurate_time_ind = db.Column(db.Integer, nullable=False, default=1)
    service_count = db.Column(db.Integer, nullable=False, default=1)
    priority = db.Column(db.Integer, nullable=False, default=2)

    service_reqs = db.relationship('ServiceReq', lazy='joined', order_by='ServiceReq.sr_id')
    cs = db.relationship('CitizenState', lazy='joined')
    office = db.relationship('Office', lazy='joined')

    def __repr__(self):
        return '<Citizen Name:(name={self.citizen_name!r})>'.format(self=self)

    def __init__(self, **kwargs):
        super(Citizen, self).__init__(**kwargs)

    def get_active_service_request(self):
        for sr in self.service_reqs:
            if sr.sr_state.sr_code != 'Complete':
                return sr

        return None

    def get_service_start_time(self):
        time_end = self.start_time

        # If a service request already exists, then the start time for the next
        # service should be the end time of the previous service request
        for s in self.service_reqs:
            sorted_periods = sorted(s.periods, key=lambda p: p.time_start)

            if len(sorted_periods) > 0 and sorted_periods[-1].time_end is not None and sorted_periods[-1].time_end > time_end:
                time_end = sorted_periods[-1].time_end

        return time_end
