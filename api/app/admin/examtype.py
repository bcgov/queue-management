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

from app.models.bookings import ExamType
from .base import Base
from flask_login import current_user
from qsystem import db


class ExamTypeConfig(Base):
    roles_allowed = ['SUPPORT']

    def is_accessible(self):
        return  current_user.is_authenticated and current_user.role.role_code in self.roles_allowed

    def get_query(self):
        return self.session.query(self.model)

    create_modal = False
    edit_modal = False
    column_list = [
        'exam_type_name',
        'exam_color',
        'number_of_hours',
        'method_type',
        'ita_ind',
        'group_exam_ind'
    ]

    column_searchable_list = {'exam_type_name'}

    form_excluded_columns = [
        'exam'
    ]

    form_create_rules = (
        'exam_type_name',
        'exam_color',
        'number_of_hours',
        'method_type',
        'ita_ind',
        'group_exam_ind'
    )

    form_edit_rules = (
        'exam_type_name',
        'exam_color',
        'number_of_hours',
        'method_type',
        'ita_ind',
        'group_exam_ind'
    )

    column_sortable_list = [
        'exam_type_name',
        'exam_color',
        'number_of_hours',
        'method_type',
        'ita_ind',
        'group_exam_ind'
    ]

    column_default_sort = 'exam_type_name'


ExamTypeModelView = ExamTypeConfig(ExamType, db.session)

