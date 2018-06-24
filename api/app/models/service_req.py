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
from sqlalchemy import BigInteger, Integer

class ServiceReq(Base):

    sr_id       = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    citizen_id  = db.Column(db.Integer, db.ForeignKey('citizen.citizen_id'), nullable=False)
    quantity    = db.Column(db.Integer, default=1, nullable=False)
    service_id  = db.Column(db.Integer, db.ForeignKey('service.service_id'), nullable=False)
    sr_state_id = db.Column(db.Integer, db.ForeignKey('srstate.sr_state_id'), nullable=False)

    periods     = db.relationship('Period', backref=db.backref("request_periods", lazy=False))
    sr_state    = db.relationship('SRState', backref=db.backref("request_states", lazy=False))
    service     = db.relationship('Service')

    def __init__(self, **kwargs):
        super(ServiceReq, self).__init__(**kwargs)

    #def getActiveServicePeriod():

    #def getTicketNumber():
