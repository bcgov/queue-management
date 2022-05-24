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


class ExamType(Base):

    exam_type_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    exam_type_name = db.Column(db.String(50), nullable=False)
    exam_color = db.Column(db.String(10), nullable=False)
    number_of_hours = db.Column(db.Integer, nullable=False)
    number_of_minutes = db.Column(db.Integer, nullable=True, default=0)
    method_type = db.Column(db.String(10), nullable=False)
    ita_ind = db.Column(db.Integer, nullable=False)
    group_exam_ind = db.Column(db.Integer,  nullable=False)
    pesticide_exam_ind = db.Column(db.Integer, nullable=False)
    deleted = db.Column(db.DateTime, nullable=True)

    # changed lazy=false to lazy=raise
    exam = db.relationship("Exam", lazy='raise')

    # changed lazy4-false to no lazy option
    #exam = db.relationship("Exam", lazy=False)

    def __repr__(self):
        return '<Exam Type Name: (name={self.exam_type_name!r})>'.format(self=self)

    def __init__(self, **kwargs):
        super(ExamType, self).__init__(**kwargs)
