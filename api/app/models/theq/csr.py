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

from qsystem import cache, db
from app.models.theq import Base


class CSR(Base):

    csr_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    username = db.Column(db.String(150), nullable=False, unique=True)
    office_id = db.Column(db.Integer, db.ForeignKey('office.office_id'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.role_id'), nullable=False)
    qt_xn_csr_ind = db.Column(db.Integer, nullable=False)
    receptionist_ind = db.Column(db.Integer, nullable=False)
    deleted = db.Column(db.DateTime, nullable=True)
    csr_state_id = db.Column(db.Integer, db.ForeignKey('csrstate.csr_state_id'), nullable=False)

    role = db.relationship("Role", lazy='joined')
    office = db.relationship("Office", lazy='joined')
    periods = db.relationship("Period", primaryjoin="and_(CSR.csr_id==Period.csr_id,Period.time_end.is_(None))",
                              order_by='desc(Period.time_start)')

    format_string = 'csr_detail_%s'

    def __repr__(self):
        return self.username

    def __init__(self, **kwargs):
        super(CSR, self).__init__(**kwargs)

    @classmethod
    def find_by_username(cls, username):
        key = CSR.format_string % username
        if cache.get(key):
            csr = cache.get(key)
            print("==> find_by_username: C: Yes, username: " + username + "; key: " + key + "; U: " + \
                  csr.username + "; O: " + csr.office.office_name)
            return cache.get(key)

        csr = CSR.query.filter(CSR.deleted.is_(None)).filter_by(username=username.split("idir/")[-1]).first()
        print("==> find_by_username: C: No, username: " + username + "; key: " + key + "; U: " + \
              csr.username + "; O: " + csr.office.office_name)
        cache.set(key, csr)
        return csr

    @classmethod
    def find_by_userid(cls, userid):
        csr = CSR.query.filter(CSR.deleted.is_(None)).filter_by(csr_id=userid).first()
        key = CSR.format_string % csr.username
        if cache.get(key):
            csr = cache.get(key)
            print("==> find_by_userid: C: Yes, userid: " + userid + "; key: " + key + "; U: " + \
                  csr.username + "; O: " + csr.office.office_name)
            return cache.get(key)

        print("==> find_by_userid: C: No, userid: " + userid + "; key: " + key + "; U: " + \
              csr.username + "; O: " + csr.office.office_name)
        cache.set(key, csr)
        return csr

    @classmethod
    def delete_user_cache(cls, username):
        key = CSR.format_string % username
        cache.delete(key)

    @classmethod
    def update_user_cache(cls, userid):
        csr_cache_before = CSR.find_by_userid(userid)
        csr_db = CSR.query.filter_by(csr_id=userid).first()
        key = CSR.format_string % csr_db.username
        cache.set(key, csr_db)
        csr_cache_after = CSR.find_by_userid(userid)
        print("==> update_user_cache: Key: " + key + "; CB: " + csr_cache_before.office.office_name + \
              "; DB: " + csr_db.office.office_name + "; CA: " + \
              csr_cache_after.office.office_name)

    def get_id(self):
        return str(self.csr_id)
