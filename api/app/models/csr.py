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

from qsystem import db, cache
from .base import Base


class CSR(Base):

    csr_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    username = db.Column(db.String(150), nullable=False)
    office_id = db.Column(db.Integer, db.ForeignKey('office.office_id'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.role_id'), nullable=False)
    qt_xn_csr_ind = db.Column(db.Integer, nullable=False)
    receptionist_ind = db.Column(db.Integer, nullable=False)
    deleted = db.Column(db.DateTime, nullable=True)
    csr_state_id = db.Column(db.Integer, db.ForeignKey('csrstate.csr_state_id'), nullable=False)

    office = db.relationship("Office", lazy='joined')
    periods = db.relationship("Period", primaryjoin="and_(CSR.csr_id==Period.csr_id,Period.time_end.is_(None))",
                              lazy='joined', order_by='desc(Period.time_start)')

    def __repr__(self):
        return self.username

    def __init__(self, **kwargs):
        super(CSR, self).__init__(**kwargs)

    @classmethod
    @cache.memoize(timeout=300)
    def find_by_username(cls, username):
        csr = CSR.query.filter_by(username=username.split("idir/")[-1]).first()
        return csr
