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


class Counter(Base):

    counter_id = db.Column(db.Integer, primary_key=True,
                           autoincrement=True, nullable=False)
    office_id = db.Column(db.Integer, db.ForeignKey(
        "office.office_id"), nullable=False)
    counter_name = db.Column(db.String(50), nullable=False)

    office = db.relationship("Office")

    def __repr__(self):
        return '<Counter Name: (name={self.counter_name!r})>'.format(self=self)

    def __init__(self, **kwargs):
        super(Exam, self).__init__(**kwargs)
