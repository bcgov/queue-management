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
from app.models.theq import Base, Period, PeriodState
from datetime import datetime
from app.utilities.snowplow import SnowPlow


class ServiceReq(Base):

    sr_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    citizen_id = db.Column(db.Integer, db.ForeignKey('citizen.citizen_id'), nullable=False)
    quantity = db.Column(db.Integer, default=1, nullable=False)
    channel_id = db.Column(db.Integer, db.ForeignKey('channel.channel_id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service.service_id'), nullable=False)
    sr_state_id = db.Column(db.Integer, db.ForeignKey('srstate.sr_state_id'), nullable=False)
    sr_number = db.Column(db.Integer, default=1, nullable=False)

    channel = db.relationship('Channel')
    periods = db.relationship('Period', backref=db.backref("request_periods", lazy=False), lazy='joined', order_by='Period.period_id')
    sr_state = db.relationship('SRState', lazy='joined')
    citizen = db.relationship('Citizen')
    service = db.relationship('Service', lazy='joined')

    # Defining String constants to appease SonarQube
    being_served_const = "Being Served"

    def __init__(self, **kwargs):
        super(ServiceReq, self).__init__(**kwargs)

    def get_active_period(self):
        sorted_periods = sorted(self.periods, key=lambda p: p.period_id)

        return sorted_periods[-1]

    def invite(self, csr, invite_type, sr_count = 1):
        active_period = self.get_active_period()
        if active_period.ps.ps_name in ["Invited", self.being_served_const, "On hold"]:
            raise TypeError("You cannot invite a citizen that has already been invited")

        #  If a generic invite type, event is either invitecitizen or returninvite.
        if invite_type == "generic":
            #  If only one SR, one period, an invitecitizen call, from First Time in Line state.
            if sr_count == 1 and len(self.periods) == 2:
                snowplow_event = "invitecitizen"
            #  Otherwise from the Back in Line state.
            else:
                snowplow_event = "returninvite"

        #  A specific invite type.  Event is invitefromlist, returnfromlist or invitefromhold
        else:
            #  If only one SR, one period, an invitefromlist call, from First Time in Line state.
            if sr_count == 1 and len(self.periods) == 2:
                snowplow_event = "invitefromlist"
            #  Either from back in line or hold state.
            else:
                if active_period.ps.ps_name == "Waiting":
                    snowplow_event = "returnfromlist"
                else:
                    snowplow_event = "invitefromhold"

        active_period.time_end = datetime.utcnow()
        # db.session.add(active_period)

        period_state_invite = PeriodState.get_state_by_name("Invited")

        new_period = Period(
            sr_id=self.sr_id,
            csr_id=csr.csr_id,
            reception_csr_ind=csr.receptionist_ind,
            ps_id=period_state_invite.ps_id,
            time_start=datetime.utcnow()
        )

        self.periods.append(new_period)

        SnowPlow.snowplow_event(self.citizen_id, csr, snowplow_event, current_sr_number=self.sr_number)

    def add_to_queue(self, csr, snowplow_event):

        active_period = self.get_active_period()
        active_period.time_end = datetime.utcnow()
        #db.session.add(active_period)

        period_state_waiting = PeriodState.get_state_by_name("Waiting")

        new_period = Period(
            sr_id=self.sr_id,
            csr_id=csr.csr_id,
            reception_csr_ind=csr.receptionist_ind,
            ps_id=period_state_waiting.ps_id,
            time_start=datetime.utcnow()
        )
        self.periods.append(new_period)

        SnowPlow.snowplow_event(self.citizen_id, csr, snowplow_event, current_sr_number=self.sr_number)

    def remove_from_queue(self):
        service_req_ids = [int(x.period_id) for x in self.periods]
        Period.delete_periods(service_req_ids)

    def begin_service(self, csr, snowplow_event):
        active_period = self.get_active_period()
        
        if active_period.ps.ps_name in [self.being_served_const]:
            raise TypeError("You cannot begin serving a citizen that is already being served")

        active_period.time_end = datetime.utcnow()
        # db.session.add(active_period)

        period_state_being_served = PeriodState.get_state_by_name(self.being_served_const)

        new_period = Period(
            sr_id=self.sr_id,
            csr_id=csr.csr_id,
            reception_csr_ind=csr.receptionist_ind,
            ps_id=period_state_being_served.ps_id,
            time_start=datetime.utcnow()
        )

        self.periods.append(new_period)

        #  Calculate number of active periods, for Snowplow call.
        period_count = len(self.periods)
        SnowPlow.snowplow_event(self.citizen_id, csr, snowplow_event, period_count = period_count,
                                current_sr_number = self.sr_number)

    def place_on_hold(self, csr):
        active_period = self.get_active_period()
        active_period.time_end = datetime.utcnow()
        # db.session.add(active_period)

        period_state_on_hold = PeriodState.get_state_by_name("On hold")

        new_period = Period(
            sr_id=self.sr_id,
            csr_id=csr.csr_id,
            reception_csr_ind=csr.receptionist_ind,
            ps_id=period_state_on_hold.ps_id,
            time_start=datetime.utcnow()
        )

        self.periods.append(new_period)

        SnowPlow.snowplow_event(self.citizen_id, csr, "hold", current_sr_number = self.sr_number)

    def finish_service(self, csr, clear_comments=True):
        active_period = self.get_active_period()
        active_period.time_end = datetime.utcnow()
        if clear_comments:
            self.citizen.citizen_comments = None
        # db.session.add(active_period)
