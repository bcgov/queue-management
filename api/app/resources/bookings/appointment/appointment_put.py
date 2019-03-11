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
from flask_restplus import Resource
from qsystem import api, db, jwt
from app.models.bookings import Appointment
from app.models.theq import CSR
from app.schemas.bookings import AppointmentSchema


@api.route("/appointments/<int:id>/", methods=["PUT"])
class AppointmentPut(Resource):

    appointment_schema = AppointmentSchema()

    @jwt.requires_auth
    def put(self, id):

        print("==> In Python PUT /appointments/<id>/ endpoint")

        csr = CSR.find_by_username(g.jwt_oidc_token_info['preferred_username'])

        json_data = request.get_json()

        if not json_data:
            return  {"message": "No input data received for updating an appointment"}

        appointment = Appointment.query.filter_by(appointment_id=id)\
                                       .filter_by(office_id=csr.office_id)\
                                       .first_or_404()

        appointment, warning = self.appointment_schema.load(json_data, instance=appointment, partial=True)

        if warning:
            logging.warning("WARNING: %s", warning)
            return {"message": warning}, 422

        db.session.add(appointment)
        db.session.commit()

        result = self.appointment_schema.dump(appointment)

        return {"appointment": result.data,
                    "errors": result.errors}, 200
