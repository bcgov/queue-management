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


class Role(Base):

    role_permission = db.Table('role_permission',
            db.Column('role_id', db.Integer, db.ForeignKey('role.role_id'), primary_key=True, nullable=False),
            db.Column('permission_id', db.Integer, db.ForeignKey('permission.permission_id'), primary_key=True, nullable=False))

    role_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_code = db.Column(db.String(100))
    role_desc = db.Column(db.String(1000))

    roles = db.relationship('CSR', lazy=False)

    def __repr__(self):
        return self.role_code

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
