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

from flask_restplus import fields
from qsystem import api, db
from .base import Base 
from sqlalchemy import BigInteger, Integer, DateTime

class Period(Base):

    period_id           = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    sr_id               = db.Column(db.Integer, db.ForeignKey('servicereq.sr_id'), nullable=False)
    csr_id              = db.Column(db.Integer, db.ForeignKey('csr.csr_id'), nullable=False)
    reception_csr_ind   = db.Column(db.Integer, nullable=False)
    channel_id          = db.Column(db.Integer, db.ForeignKey('channel.channel_id'), nullable=False)
    ps_id               = db.Column(db.Integer, db.ForeignKey('periodstate.ps_id'), nullable=False)
    time_start          = db.Column(db.DateTime, nullable=False)
    time_end            = db.Column(db.DateTime, nullable=True)
    accurate_time_ind   = db.Column(db.Integer, nullable=False)

    period_state        = db.relationship("PeriodState", backref=db.backref("state_periods", lazy=False))
    channel             = db.relationship("Channel", backref=db.backref("channel_periods", lazy=False))

    def __repr__(self):
        return '<Period id:(name={self.period_id!r})>'.format(self=self)

    def __init__(self, **kwargs):
        super(Period, self).__init__(**kwargs)
