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

from app.models.bookings import Booking, Room
from .base import Base
from flask import flash, request
from flask_admin.babel import gettext
from flask_admin.model.helpers import get_mdict_item_or_list
from flask_login import current_user
from qsystem import db
from datetime import datetime
import pytz


class RoomConfig(Base):
    roles_allowed = ['SUPPORT', 'GA']

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role.role_code in self.roles_allowed

    def get_query(self):
        if current_user.role.role_code == 'SUPPORT':
            return self.session.query(self.model)
        elif current_user.role.role_code == 'GA':
            return self.session.query(self.model).filter_by(office_id=current_user.office_id)

    def on_model_change(self, form, model, is_created):

        if not is_created:
            room_id = get_mdict_item_or_list(request.args, 'id')
            today = datetime.now()
            today_aware = pytz.utc.localize(today)

            booking_room = Booking.query.filter_by(room_id=room_id)\
                                        .filter(Booking.start_time > today_aware).count()

            specific_room = Room.query.filter_by(room_id=room_id).first()
            room_name = specific_room.room_name

            if model.deleted is not None and booking_room > 0:
                message = "'" + room_name + "' is currently being used for bookings. " \
                                        "Reschedule bookings that use this room before setting the deleted date."
                flash(gettext(message), 'warning')
                model.deleted = None
                form.deleted.data = None

    create_modal = False
    edit_modal = False
    can_delete = False

    # Defining String constants to appease SonarQube
    office_name_const = 'office.office_name'

    column_list = [
        office_name_const,
        'room_name',
        'capacity',
        'color',
        'deleted'
    ]

    form_excluded_columns = [
        'sb',
        'booking'
    ]

    column_labels = {office_name_const: 'Office Name',
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
        office_name_const
    ]

    column_searchable_list = {
        office_name_const
    }
    

RoomModelView = RoomConfig(Room, db.session)
