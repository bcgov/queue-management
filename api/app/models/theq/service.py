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
import enum
from sqlalchemy import Enum
from app.utilities.yesno import YesNo


class Availability(enum.Enum):
    SHOW = 'SHOW'
    HIDE = 'HIDE'
    DISABLE = 'DISABLE'


class Service(Base):

    service_metadata = db.Table('service_metadata',
                db.Column('service_id', db.Integer, db.ForeignKey('service.service_id'), primary_key=True, nullable=False),
                db.Column('metadata_id', db.Integer,db.ForeignKey('metadata.metadata_id'), primary_key=True, nullable=False))

    service_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    service_code = db.Column(db.String(50), nullable=False)
    service_name = db.Column(db.String(500), nullable=False)
    service_desc = db.Column(db.String(2000), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('service.service_id'), nullable=True)
    deleted = db.Column(db.DateTime, nullable=True)
    prefix = db.Column(db.String(10), nullable=False)
    display_dashboard_ind = db.Column(db.Integer, nullable=False)
    actual_service_ind = db.Column(db.Integer, nullable=False)

    external_service_name = db.Column(db.String(100), nullable=True)
    online_link = db.Column(db.String(200), nullable=True)
    online_availability = db.Column(Enum(Availability))
    timeslot_duration = db.Column(db.Integer, nullable=True)
    is_dlkt = db.Column(Enum(YesNo))
    email_paragraph = db.Column(db.String(2000), nullable=True)
    css_colour = db.Column(db.String(50), nullable=True)
    partner = db.Column(db.String(), nullable=True)
    program = db.Column(db.String(), nullable=True)
    recoverable = db.Column(db.String(), nullable=True)

    offices = db.relationship("Office", secondary='office_service')
    parent = db.relationship("Service", remote_side=[service_id])

    def __repr__(self):
        return self.service_name

    def __init__(self, **kwargs):
        super(Service, self).__init__(**kwargs)
