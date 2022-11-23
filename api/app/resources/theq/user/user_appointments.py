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
from flask import g
from flask_restx import Resource
from sqlalchemy import exc

from app.models.theq import PublicUser
from app.schemas.bookings import AppointmentSchema
from qsystem import api
from app.utilities.auth_util import Role, has_any_role
from app.auth.auth import jwt


@api.route("/users/appointments/", methods=["GET"])
class UserAppointments(Resource):
    appointments_schema = AppointmentSchema(many=True)

    @jwt.has_one_of_roles([Role.online_appointment_user.value])
    def get(self):

        # Get all appointments for the citizen
        try:
            appointments = PublicUser.find_appointments_by_username(g.jwt_oidc_token_info['username'])

            result = self.appointments_schema.dump(appointments)
            return {'appointments': result}

        except exc.SQLAlchemyError as exception:
            logging.exception(exception)
            return {'message': 'API is down'}, 500
