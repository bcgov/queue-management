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
        return current_user.is_authenticated and current_user.role.role_code in self.roles_allowed

    def get_query(self):
        return self.session.query(self.model)

    create_modal = False
    edit_modal = False
    can_delete = False

    column_list = [
        'exam_type_name',
        'exam_color',
        'number_of_hours',
        'number_of_minutes',
        'method_type',
        'ita_ind',
        'group_exam_ind',
        'pesticide_exam_ind',
        'deleted'
    ]

    column_labels = {
        'exam_type_name': 'Exam Type Name',
        'exam_color': 'Exam Color',
        'number_of_hours': 'Number of Hours',
        'number_of_minutes': 'Number of Minutes',
        'method_type': 'Method Type',
        'ita_ind': 'SkilledTradesBC',
        'group_exam_ind': 'Group Exam Flag',
        'pesticide_exam_ind': 'Environment Exam Flag',
        'deleted': 'Deleted',
    }

    column_searchable_list = {'exam_type_name'}

    form_excluded_columns = [
        'exam'
    ]

    form_create_rules = (
        'exam_type_name',
        'exam_color',
        'number_of_hours',
        'number_of_minutes',
        'method_type',
        'ita_ind',
        'group_exam_ind',
        'pesticide_exam_ind',
        'deleted'
    )

    form_edit_rules = {
        'exam_type_name': 'Exam Type Name',
        'exam_color': 'Exam Color',
        'number_of_hours': 'Number of Hours',
        'number_of_minutes': 'Number of Minutes',
        'method_type': 'Method Type',
        'ita_ind': 'ITA Exam Flag',
        'group_exam_ind': 'Group Exam Flag',
        'pesticide_exam_ind': 'Environment Exam Flag',
        'deleted': 'Deleted',
    }
    form_choices = {
        'ita_ind': [
            ("0", 'No - this is not an ITA exam'), ("1", 'Yes - this is an ITA exam')
        ],
        'group_exam_ind': [
            ("0", 'No - this is not a Group exam'), ("1", 'Yes - this is a Group exam')
        ],
        'pesticide_exam_ind': [
            ("0", 'No - this is not an Environment exam'), ("1", 'Yes - this is an Environment exam')
        ]
    }

    column_sortable_list = [
        'exam_type_name',
        'exam_color',
        'number_of_hours',
        'method_type',
        'ita_ind',
        'group_exam_ind',
        'pesticide_exam_ind',
        'deleted'
    ]

    column_default_sort = 'exam_type_name'


ExamTypeModelView = ExamTypeConfig(ExamType, db.session)

