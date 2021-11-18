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

from flask_restx import fields
from qsystem import api, db
from app.models.theq import Base


class Permission(Base):

    model = api.model('Permission', {
        'permission_id': fields.Integer,
        'permission_code': fields.String,
        'permission_desc': fields.String
        })

    permission_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    permission_code = db.Column(db.String(100))
    permission_desc = db.Column(db.String(1000))

    def __repr__(self):
        return '<Permission Code: %r>' % self.permission_code

    def __init__(self, **kwargs):
        super(Permission, self).__init__(**kwargs)

    def json(self, permission_id, permission_code, permission_desc):
        return {"permission_id": self.permission_id,
                "permission_code": self.permission_code,
                "permission_desc": self.permission_desc}
