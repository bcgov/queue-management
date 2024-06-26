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
import pytz
from datetime import datetime, timedelta
from flask import request
from flask_restx import Resource
from sqlalchemy import exc
from app.models.bookings import Appointment
from app.models.theq import CSR
from app.schemas.bookings import AppointmentSchema
from qsystem import api, appt_limit
from app.utilities.auth_util import Role, get_username
from app.auth.auth import jwt


@api.route("/appointments/", methods=["GET"])
class AppointmentList(Resource):

    appointment_schema = AppointmentSchema(many=True)

    @jwt.has_one_of_roles([Role.internal_user.value])
    def get(self):

        office_id = request.args.get("office_id", default=None)
        if not office_id:
            csr = CSR.find_by_username(get_username())
            office_id = csr.office_id
        appt_limit_int = int(appt_limit)     
        # today's date and time
        dt = datetime.now()
        upper_dt = dt - timedelta(days=appt_limit_int)
        filter_date = pytz.utc.localize(upper_dt)
        # print("filter_date",filter_date)
        try:
            appointments = Appointment.query.filter_by(office_id=office_id)\
                                            .filter(Appointment.start_time >= filter_date)\
                                            .all()
            result = self.appointment_schema.dump(appointments)

            return {"appointments": result,
                    "errors": {"errors": self.appointment_schema.validate(appointments)}}, 200

        except exc.SQLAlchemyError as error:
            logging.error(error, exc_info=True)
            return {"message": "API is down"}, 500
