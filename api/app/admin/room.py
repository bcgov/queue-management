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

from app.models.bookings import Room
from .base import Base
from flask_login import current_user
from qsystem import db


class RoomConfig(Base):
    roles_allowed = ['SUPPORT', 'GA']

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role.role_code in self.roles_allowed

    def get_query(self):
        if current_user.role.role_code == 'SUPPORT':
            return self.session.query(self.model)
        elif current_user.role.role_code == 'GA':
            return self.session.query(self.model).filter_by(office_id=current_user.office_id)

    create_modal = False
    edit_modal = False
    can_delete = False

    column_list = [
        'office.office_name',
        'room_name',
        'capacity',
        'color',
        'deleted'
    ]

    form_excluded_columns = [
        'sb',
        'booking'
    ]

    column_labels = {'office.office_name': 'Office Name',
                     'deleted': 'Deleted'}

    form_create_rules = (
        'office',
        'room_name',
        'capacity',
        'color',
        'deleted'
    )

    form_edit_rules = (
        'office',
        'room_name',
        'capacity',
        'color',
        'deleted'
    )

    column_sortable_list = [
        'room_name',
        'capacity',
        'color',
        'deleted',
        'office.office_name'
    ]

    column_searchable_list = {
        'office.office_name'
    }


RoomModelView = RoomConfig(Room, db.session)