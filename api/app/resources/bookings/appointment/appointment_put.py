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
from qsystem import api, db
from app.auth.auth import jwt
from app.models.bookings import Appointment
from app.models.theq import CSR, PublicUser, Citizen, Office, Service
from app.schemas.bookings import AppointmentSchema
from app.utilities.snowplow import SnowPlow
from app.utilities.auth_util import is_public_user
from app.utilities.auth_util import Role, has_any_role
from app.utilities.email import send_email, get_confirmation_email_contents
from app.services import AvailabilityService
from dateutil.parser import parse
from qsystem import socketio, application
from app.utilities.sms import send_sms

@api.route("/appointments/<int:id>/", methods=["PUT"])
class AppointmentPut(Resource):
    appointment_schema = AppointmentSchema()

    @jwt.has_one_of_roles([Role.internal_user.value, Role.online_appointment_user.value])
    def put(self, id):
        json_data = request.get_json()
        csr = None
        user = None

        if not json_data:
            return {"message": "No input data received for updating an appointment"}
        is_public_user_appt = is_public_user()

        # Should delete draft appointment, and free up slot, before booking.
        # Clear up a draft if one was previously created by user reserving this time.
        if json_data.get('appointment_draft_id'):
            draft_id_to_delete = int(json_data['appointment_draft_id'])
            Appointment.delete_draft([draft_id_to_delete])
            if not application.config['DISABLE_AUTO_REFRESH']:
                socketio.emit('appointment_delete', draft_id_to_delete)

        if is_public_user_appt:
            office_id = json_data.get('office_id')
            office = Office.find_by_id(office_id)
            # user = PublicUser.find_by_username(g.oidc_token_info['username'])
            # citizen = Citizen.find_citizen_by_username(g.oidc_token_info['username'], office_id)
            # Validate if the same user has other appointments for same day at same office
            appointments = Appointment.find_by_username_and_office_id(office_id=office_id,
                                                                      user_name=g.jwt_oidc_token_info['username'],
                                                                      start_time=json_data.get('start_time'),
                                                                      timezone=office.timezone.timezone_name,
                                                                      appointment_id=id)
            if appointments and len(appointments) >= office.max_person_appointment_per_day:
                return {"code": "MAX_NO_OF_APPOINTMENTS_REACHED",
                        "message": "Maximum number of appoinments reached"}, 400

            # Check for race condition
            start_time = parse(json_data.get('start_time'))
            end_time = parse(json_data.get('end_time'))
            service_id = json_data.get('service_id')
            service = Service.query.get(int(service_id))
            if not AvailabilityService.has_available_slots(office=office, start_time=start_time, end_time=end_time, service=service):
                return {"code": "CONFLICT_APPOINTMENT",
                        "message": "Cannot create appointment due to scheduling conflict.  Please pick another time."}, 400

        else:
            csr = CSR.find_by_username(g.jwt_oidc_token_info['username'])
            office_id = csr.office_id
            office = Office.find_by_id(office_id)

        appointment = Appointment.query.filter_by(appointment_id=id) \
            .filter_by(office_id=office_id) \
            .first_or_404()

        # If appointment is not made by same user, throw error
        if is_public_user_appt:
            citizen = Citizen.find_citizen_by_id(appointment.citizen_id)
            user = PublicUser.find_by_username(g.jwt_oidc_token_info['username'])
            # Should just match based on appointment_id and other info.  Can't have proper auth yet.
            if citizen.user_id != user.user_id:
                abort(403)

        appointment = self.appointment_schema.load(json_data, instance=appointment, partial=True)
        warning = self.appointment_schema.validate(json_data)

        if warning:
            logging.warning("WARNING: %s", warning)
            return {"message": warning}, 422

        db.session.add(appointment)
        db.session.commit()

        # Send confirmation email
        try:
            send_email(request.headers['Authorization'].replace('Bearer ', ''), *get_confirmation_email_contents(appointment, office, office.timezone, user))
            send_sms(appointment, office, office.timezone, user,
                             request.headers['Authorization'].replace('Bearer ', ''))
        except Exception as exc:
            logging.exception('Error on token generation - %s', exc)

        #   Make Snowplow call.
        schema = 'appointment_update'
        if "checked_in_time" in json_data:
            schema = 'appointment_checkin'

        if not appointment.is_draft:
            SnowPlow.snowplow_appointment(None, csr, appointment, schema)

        result = self.appointment_schema.dump(appointment)

        if not application.config['DISABLE_AUTO_REFRESH']:
            # Treat checked_in_time as a delete, as we filter those from frontend
            # this happens when checking in an appointment
            if "checked_in_time" in json_data:
                socketio.emit('appointment_delete', id)
            else:
                socketio.emit('appointment_update', result)
        

        return {"appointment": result,
                "errors": self.appointment_schema.validate(appointment)}, 200
