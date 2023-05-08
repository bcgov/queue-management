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
from sqlalchemy import exc
from flask_restx import Resource
from app.models.bookings import Appointment
from app.models.theq import CSR
from app.schemas.bookings import AppointmentSchema
from qsystem import api
from app.utilities.auth_util import Role, get_username
from app.auth.auth import jwt


@api.route("/appointments/<int:id>/", methods=["GET"])
class AppointmentDetail(Resource):

    appointment_schema = AppointmentSchema()

    @jwt.has_one_of_roles([Role.internal_user.value])
    def get(self, id):

        csr = CSR.find_by_username(get_username())

        try:
            appointment = Appointment.query.filter_by(appointment_id=id)\
                                           .filter_by(office_id=csr.office_id)\
                                           .first_or_404()

            result = self.appointment_schema.dump(appointment)

            return {"appointment": result,
                    "errors": self.appointment_schema.validate(appointment)}, 200

        except exc.SQLAlchemyError as error:
            logging.error(error, exc_info=True)
            return {"message": "API is down"}, 500
