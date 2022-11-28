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

import logging
from qsystem import cache, db, my_print
from app.models.theq import Base
from sqlalchemy import func


class CSR(Base):

    csr_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    username = db.Column(db.String(150), nullable=False, unique=True)
    office_id = db.Column(db.Integer, db.ForeignKey('office.office_id'), nullable=False)
    counter_id = db.Column(db.Integer, db.ForeignKey('counter.counter_id'), nullable=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.role_id'), nullable=False)
    qt_xn_csr_ind = db.Column(db.Integer, nullable=False, default=0) # deprecated
    receptionist_ind = db.Column(db.Integer, nullable=False)
    deleted = db.Column(db.DateTime, nullable=True)
    csr_state_id = db.Column(db.Integer, db.ForeignKey('csrstate.csr_state_id'), nullable=False)
    pesticide_designate = db.Column(db.Integer, default=0, nullable=False)
    finance_designate = db.Column(db.Integer, default=0, nullable=False)
    office_manager = db.Column(db.Integer, default=0, nullable=False)
    ita2_designate = db.Column(db.Integer, default=0, nullable=False)

    role = db.relationship("Role", lazy='joined')
    office = db.relationship("Office", lazy='joined')
    counter = db.relationship("Counter", lazy='joined')
    periods = db.relationship("Period", primaryjoin="and_(CSR.csr_id==Period.csr_id,Period.time_end.is_(None))",
                              order_by='desc(Period.time_start)')

    format_string = 'csr_detail_%s'

    def __repr__(self):
        return self.username

    def __init__(self, **kwargs):
        super(CSR, self).__init__(**kwargs)

    @classmethod
    def find_by_username(cls, username):
        #   Possible keycloak->TheQ id values are user@idir->user, idir/user->user or user@bceid->user@bceid
        idir_id = username.split("idir/")[-1].lower()
        if "@idir" in username:
            idir_id = username.split("@idir")[0].lower()
        key = CSR.format_string % idir_id
        if cache.get(key):
            return cache.get(key)

        my_print("==> In Python, csr.py, find_by_username: username=" + str(username) + "; idir_id=" + str(idir_id))
        csr = CSR.query.filter(CSR.deleted.is_(None)).filter(CSR.username==idir_id).first()

        cache.set(key, csr)
        return csr

    @classmethod
    def find_by_userid(cls, userid):
        csr = CSR.query.filter(CSR.deleted.is_(None)).filter_by(csr_id=userid).first()
        key = (CSR.format_string % csr.username).lower()
        if cache.get(key):
            return cache.get(key)

        cache.set(key, csr)
        return csr

    @classmethod
    def delete_user_cache(cls, username):
        idir_id = username.split("idir/")[-1]
        key = (CSR.format_string % idir_id).lower()
        cache.delete(key)

    @classmethod
    def update_user_cache(cls, userid):
        try:
            if type(userid) is str:
                userid = int(userid)
            csr_db = CSR.query.filter_by(csr_id=userid).first()
            key = (CSR.format_string % csr_db.username).lower()
            cache.set(key, csr_db)
        except Exception as ex:
            logging.exception("==> csr.py, update_user_cache, userid: " + str(userid) + "; type: " + str(type(userid)))
            logging.exception("    --> Exception: " + str(ex))

    def get_id(self):
        return str(self.csr_id)
