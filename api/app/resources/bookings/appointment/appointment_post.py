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
from datetime import datetime
from threading import Thread

from flask import copy_current_request_context
from flask import request, g, current_app
from flask_restx import Resource

from app.models.bookings import Appointment
from app.models.theq import CSR, CitizenState, PublicUser, Office, Service
from app.schemas.bookings import AppointmentSchema
from app.schemas.theq import CitizenSchema
from app.utilities.auth_util import Role, has_any_role
from app.utilities.auth_util import is_public_user
from app.utilities.email import get_confirmation_email_contents, send_email, get_blackout_email_contents
from app.utilities.snowplow import SnowPlow
from qsystem import api, api_call_with_retry, db, oidc, my_print
from app.services import AvailabilityService
from dateutil.parser import parse
from pprint import pprint

from qsystem import socketio

@api.route("/appointments/", methods=["POST"])
class AppointmentPost(Resource):

    appointment_schema = AppointmentSchema()
    citizen_schema = CitizenSchema()

    @oidc.accept_token(require_token=True)
    @api_call_with_retry
    @has_any_role(roles=[Role.internal_user.value, Role.online_appointment_user.value])
    def post(self):
        my_print("==> In AppointmentPost, POST /appointments/")
        json_data = request.get_json()
        if not json_data:
            return {"message": "No input data received for creating an appointment"}, 400

        is_blackout_appt = json_data.get('blackout_flag', 'N') == 'Y'
        csr = None
        user = None
        office = None

        #  Create a citizen for later use.
        citizen = self.citizen_schema.load({}).data

        # Check if the appointment is created by public user. Can't depend on the IDP as BCeID is used by other users as well
        is_public_user_appointment = is_public_user()
        if is_public_user_appointment:
            office_id = json_data.get('office_id')
            service_id = json_data.get('service_id')
            user = PublicUser.find_by_username(g.oidc_token_info['username'])
            # Add values for contact info and notes
            json_data['contact_information'] = user.email
            telephone = f'. Phone: {user.telephone}' if user.telephone else ''
            json_data['comments'] = json_data.get('comments', '') + telephone

            citizen.user_id = user.user_id
            citizen.citizen_name = user.display_name

            office = Office.find_by_id(office_id)
            service = Service.query.get(int(service_id))

            # Validate if the same user has other appointments for same day at same office
            appointments = Appointment.find_by_username_and_office_id(office_id=office_id,
                                                                      user_name=g.oidc_token_info['username'],
                                                                      start_time=json_data.get('start_time'),
                                                                      timezone=office.timezone.timezone_name)
            if appointments and len(appointments) >= office.max_person_appointment_per_day:
                return {"code": "MAX_NO_OF_APPOINTMENTS_REACHED", "message": "Maximum number of appointments reached"}, 400

            # Check for race condition
            start_time = parse(json_data.get('start_time'))
            end_time = parse(json_data.get('end_time'))
            if not AvailabilityService.has_available_slots(office=office, start_time=start_time, end_time=end_time, service=service):
                return {"code": "CONFLICT_APPOINTMENT",
                        "message": "Cannot create appointment due to conflict in time"}, 400

        else:
            csr = CSR.find_by_username(g.oidc_token_info['username'])
            office_id = csr.office_id
            office = Office.find_by_id(office_id)

        citizen.office_id = office_id
        citizen.qt_xn_citizen_ind = 0
        citizen_state = CitizenState.query.filter_by(cs_state_name="Appointment booked").first()
        citizen.cs_id = citizen_state.cs_id
        citizen.start_time = datetime.now()
        citizen.service_count = 1

        db.session.add(citizen)
        db.session.commit()

        appointment, warning = self.appointment_schema.load(json_data)
        if is_public_user_appointment:
            appointment.citizen_name = user.display_name
            appointment.online_flag = True

        if warning:
            logging.warning("WARNING: %s", warning)
            return {"message": warning}, 422

        if appointment.office_id == office_id:
            appointment.citizen_id = citizen.citizen_id
            db.session.add(appointment)
            db.session.commit()

            # If staff user is creating a blackout event then send email to all of the citizens with appointments for that period
            if is_blackout_appt:
                appointment_ids_to_delete = []
                appointments_for_the_day = Appointment.get_appointment_conflicts(office_id, json_data.get('start_time'),
                                                                                 json_data.get('end_time'))
                for (cancelled_appointment, office, timezone, user) in appointments_for_the_day:
                    if cancelled_appointment.appointment_id != appointment.appointment_id and not cancelled_appointment.checked_in_time:
                        appointment_ids_to_delete.append(cancelled_appointment.appointment_id)

                        # Send blackout email
                        @copy_current_request_context
                        def async_email(subject, email, sender, body):
                            return send_email(subject, email, sender, body)

                        thread = Thread(target=async_email, args=get_blackout_email_contents(appointment, cancelled_appointment, office, timezone, user))
                        thread.daemon = True
                        thread.start()

                # Delete appointments
                if len(appointment_ids_to_delete) > 0:
                    Appointment.delete_appointments(appointment_ids_to_delete)

            else:
                # Send confirmation email
                @copy_current_request_context
                def async_email(subject, email, sender, body):
                    send_email(subject, email, sender, body)

                thread = Thread(target=async_email, args=get_confirmation_email_contents(appointment, office, office.timezone, user))
                thread.daemon = True
                thread.start()

            SnowPlow.snowplow_appointment(citizen, csr, appointment, 'appointment_create')

            pprint(appointment)
            result = self.appointment_schema.dump(appointment)

            socketio.emit('appointment_refresh')

            return {"appointment": result.data,
                    "errors": result.errors}, 201

        else:
            return {"The Appointment Office ID and CSR Office ID do not match!"}, 403
