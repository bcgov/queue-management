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
from flask_restx import Resource
from flask import request, g
from app.schemas.bookings import AppointmentSchema
from app.schemas.theq import CitizenSchema
from app.models.theq import CSR, CitizenState
from qsystem import api, api_call_with_retry, db, oidc
from app.utilities.snowplow import SnowPlow
from datetime import datetime

@api.route("/appointments/", methods=["POST"])
class AppointmentPost(Resource):

    appointment_schema = AppointmentSchema()
    citizen_schema = CitizenSchema()

    @oidc.accept_token(require_token=True)
    @api_call_with_retry
    def post(self):

        csr = CSR.find_by_username(g.oidc_token_info['username'])

        #  Create a citizen for later use.
        citizen = self.citizen_schema.load({}).data
        citizen.office_id = csr.office_id
        citizen.qt_xn_citizen_ind = 0;
        citizen_state = CitizenState.query.filter_by(cs_state_name="Appointment booked").first()
        citizen.cs_id = citizen_state.cs_id
        citizen.start_time = datetime.now()
        citizen.service_count = 1
        db.session.add(citizen)
        db.session.commit()

        json_data = request.get_json()

        if not json_data:
            return {"message": "No input data received for creating an appointment"}, 400

        appointment, warning = self.appointment_schema.load(json_data)

        if warning:
            logging.warning("WARNING: %s", warning)
            return {"message": warning}, 422

        if appointment.office_id == csr.office_id:
            appointment.citizen_id = citizen.citizen_id
            db.session.add(appointment)
            db.session.commit()

            SnowPlow.snowplow_appointment(citizen, csr, appointment, 'appointment_create')

            result = self.appointment_schema.dump(appointment)

            return {"appointment": result.data,
                    "errors": result.errors}, 201

        else:
            return {"The Appointment Office ID and CSR Office ID do not match!"}, 403
