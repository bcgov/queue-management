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
from typing import List

from flask import g, request
from flask_restx import Resource
from sqlalchemy import exc

from app.auth.auth import jwt
from app.models.bookings.appointments import Appointment as AppointmentModel
from app.models.theq import PublicUser as PublicUserModel
from app.schemas.theq import UserSchema
from app.utilities.auth_util import Role, get_username
from app.utilities.sms import send_sms
from qsystem import api, db

# Defining String constants to appease SonarQube
api_down_const = 'API is down'


def _token_last_name(user_info):
    return user_info.get('family_name') or user_info.get('lastName') or ''


def _normalize_user_defaults(user: PublicUserModel):
    if user.last_name is None:
        user.last_name = ''
    if user.telephone is None:
        user.telephone = ''
    if user.send_email_reminders is None:
        user.send_email_reminders = False
    if user.send_sms_reminders is None:
        user.send_sms_reminders = False

@api.route("/users/", methods=['POST'])
class PublicUsers(Resource):
    user_schema = UserSchema(many=False)

    @jwt.has_one_of_roles([Role.online_appointment_user.value])
    def post(self):
        try:
            user_info = g.jwt_oidc_token_info
            username = get_username()
            user: PublicUserModel = PublicUserModel.find_by_username(username)
            if not user:
                user = PublicUserModel()
                user.username = username
                user.email = user_info.get('email')
            else:  # update email only if the email is None for existing user
                if not user.email:
                    user.email = user_info.get('email')
            user.display_name = user_info.get('display_name')
            if not user.last_name:
                user.last_name = _token_last_name(user_info)
            _normalize_user_defaults(user)
            db.session.add(user)
            db.session.commit()

            result = [self.user_schema.dump(user)]
            return result, 200

        except exc.SQLAlchemyError as exception:
            logging.exception(exception)
            return {'message': api_down_const}, 500


@api.route("/users/<int:user_id>/", methods=['PUT'])
class PublicUser(Resource):
    user_schema = UserSchema(many=False)

    @jwt.has_one_of_roles([Role.online_appointment_user.value])
    def put(self, user_id: int):
        try:
            json_data = request.get_json()
            username = get_username()
            user: PublicUserModel = PublicUserModel.find_by_username(username)
            current_sms_reminder: bool = user.send_sms_reminders
            user.email = json_data.get('email')
            user.telephone = json_data.get('telephone')
            user.send_email_reminders = json_data.get('send_email_reminders')
            user.send_sms_reminders = json_data.get('send_sms_reminders')
            db.session.add(user)
            db.session.commit()

            # If the user is opting in for SMS reminders, send reminders for all the appointments.
            if not current_sms_reminder and user.send_sms_reminders:
                appointments: List[AppointmentModel] = PublicUserModel.find_appointments_by_username(
                    username)
                for appointment in appointments:
                    office = appointment.office
                    send_sms(appointment, office, office.timezone, user,
                             request.headers['Authorization'].replace('Bearer ', ''))

            result = [self.user_schema.dump(user)]
            return result, 200

        except exc.SQLAlchemyError as exception:
            logging.exception(exception)
            return {'message': api_down_const}, 500


@api.route("/users/me/", methods=['GET'])
class CurrentUser(Resource):
    user_schema = UserSchema(many=False)

    @jwt.has_one_of_roles([Role.online_appointment_user.value])
    def get(self):
        try:
            user: PublicUserModel = PublicUserModel.find_by_username(get_username())

            result = [self.user_schema.dump(user)]
            return result, 200

        except exc.SQLAlchemyError as exception:
            logging.exception(exception)
            return {'message': api_down_const}, 500
