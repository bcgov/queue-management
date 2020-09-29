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
import datetime, pytz
from flask import g
from flask_restx import Resource
from sqlalchemy import exc
from app.models.bookings import Appointment
from app.models.theq import CSR
from app.schemas.bookings import AppointmentSchema
from qsystem import api, oidc
from app.utilities.auth_util import Role, has_any_role


@api.route("/appointments/", methods=["GET"])
class AppointmentList(Resource):

    appointment_schema = AppointmentSchema(many=True)

    @oidc.accept_token(require_token=True)
    @has_any_role(roles=[Role.internal_user.value])
    def get(self):

        csr = CSR.find_by_username(g.oidc_token_info['username'])
              
        # today's date and time
        today = datetime.datetime.now()
        dt = pytz.utc.localize(today)
        today_year = dt.year
        today_month = dt.month
        first_month = datetime.datetime(today_year, today_month, 1, 0, 0, 0, 0)
        filter_date = pytz.utc.localize(first_month)
        """ print("first of the month is .... ") """
        """ print(first_month) """

        try:
            appointments = Appointment.query.filter_by(office_id=csr.office_id)\
                                            .filter(Appointment.start_time >= filter_date)\
                                            .all()
            result = self.appointment_schema.dump(appointments)

            return {"appointments": result.data,
                    "errors": result.errors}, 200

        except exc.SQLAlchemyError as error:
            logging.error(error, exc_info=True)
            return {"message": "API is down"}, 500
