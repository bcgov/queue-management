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


class Invigilator(Base):

    invigilator_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    office_id = db.Column(db.Integer, db.ForeignKey("office.office_id"), nullable=False)
    invigilator_name = db.Column(db.String(50), nullable=False)
    invigilator_notes = db.Column(db.String(400), nullable=True)
    contact_phone = db.Column(db.String(15), nullable=True)
    contact_email = db.Column(db.String(50), nullable=True)
    contract_number = db.Column(db.String(50), nullable=False)
    contract_expiry_date = db.Column(db.String(50), nullable=False)
    deleted = db.Column(db.DateTime, nullable=True)
    shadow_count = db.Column(db.Integer, default=2, nullable=False)
    shadow_flag = db.Column(db.String(1), default='Y', nullable=False)

    office = db.relationship("Office", lazy="joined")

    def __repr__(self):
        return '<Invigilator Name: (name={self.invigilator_name!r})>'.format(self=self)

    def __init__(self, **kwargs):
        super(Invigilator, self).__init__(**kwargs)
