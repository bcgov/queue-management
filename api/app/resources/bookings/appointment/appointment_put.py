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
from flask import request, g, abort
from flask_restx import Resource
from qsystem import api, db, oidc
from app.models.bookings import Appointment
from app.models.theq import CSR, PublicUser, Citizen, Office
from app.schemas.bookings import AppointmentSchema
from app.utilities.snowplow import SnowPlow
from app.utilities.auth_util import is_public_user


@api.route("/appointments/<int:id>/", methods=["PUT"])
class AppointmentPut(Resource):

    appointment_schema = AppointmentSchema()

    @oidc.accept_token(require_token=True)
    def put(self, id):
        json_data = request.get_json()
        csr = None
        is_blackout_appt = json_data.get('blackout_flag', 'N') == 'Y'
        if not json_data:
            return {"message": "No input data received for updating an appointment"}
        is_public_user_appt = is_public_user()
        if is_public_user_appt:
            office_id = json_data.get('office_id')
            office = Office.find_by_id(office_id)
            # user = PublicUser.find_by_username(g.oidc_token_info['username'])
            citizen = Citizen.find_citizen_by_username(g.oidc_token_info['username'], office_id)
            # Validate if the same user has other appointments for same day at same office
            appointments = Appointment.find_by_citizen_id_and_office_id(office_id=office_id,
                                                                        citizen_id=citizen.citizen_id,
                                                                        start_time=json_data.get('start_time'),
                                                                        timezone=office.timezone.timezone_name,
                                                                        appointment_id=id)
            if appointments and len(appointments) >= office.max_person_appointment_per_day:
                return {"code": "MAX_NO_OF_APPOINTMENTS_REACHED",
                        "message": "Maximum number of appoinments reached"}, 400
        else:
            csr = CSR.find_by_username(g.oidc_token_info['username'])
            office_id = csr.office_id

        # if not is_blackout_appt:
        #     # Check if there is an appointment for this time
        #     conflict_appointments = Appointment.get_appointment_conflicts(office_id, json_data.get('start_time'),
        #                                                                       json_data.get('end_time'), appointment_id=id)
        #     if conflict_appointments:
        #         return {"code": "CONFLICT", "message": "Conflict while creating appointment"}, 400

        appointment = Appointment.query.filter_by(appointment_id=id)\
                                       .filter_by(office_id=office_id)\
                                       .first_or_404()

        # If appointment is not made by same user, throw error
        if is_public_user_appt and appointment.citizen_id != citizen.citizen_id:
            abort(403)

        appointment, warning = self.appointment_schema.load(json_data, instance=appointment, partial=True)

        if warning:
            logging.warning("WARNING: %s", warning)
            return {"message": warning}, 422

        db.session.add(appointment)
        db.session.commit()

        #   Make Snowplow call.
        schema = 'appointment_update'
        if "checked_in_time" in json_data:
            schema = 'appointment_checkin'

        #TODO handle public user login
        if csr:
            SnowPlow.snowplow_appointment(None, csr, appointment, schema)

        result = self.appointment_schema.dump(appointment)

        return {"appointment": result.data,
                    "errors": result.errors}, 200
