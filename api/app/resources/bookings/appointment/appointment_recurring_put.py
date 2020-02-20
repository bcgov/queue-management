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
from flask import request, g
from flask_restx import Resource
from qsystem import api, db, oidc
from app.models.bookings import Appointment
from app.models.theq import CSR
from app.schemas.bookings import AppointmentSchema


@api.route("/appointments/recurring/<string:id>", methods=["PUT"])
class AppointmentRecurringPut(Resource):

    appointment_schema = AppointmentSchema()

    @oidc.accept_token(require_token=True)
    def put(self, id):

        csr = CSR.find_by_username(g.oidc_token_info['username'])

        json_data = request.get_json()

        if not json_data:
            return {"message": "No input data received for updating an series of appointments"}

        appointments = Appointment.query.filter_by(recurring_uuid=id)\
                                  .filter_by(office_id=csr.office_id)\
                                  .all()

        for appointment in appointments:

            appointment, warning = self.appointment_schema.load(json_data, instance=appointment, partial=True)

            if warning:
                logging.warning('WARNING: %s', warning)
                return {"message": warning}, 422

            db.session.add(appointment)
            db.session.commit()

        result = self.appointment_schema.dump(appointments)

        return {
            "appointments": result.data,
            "errors": result.errors
        }, 200
