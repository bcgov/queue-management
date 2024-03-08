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

from dateutil.parser import parse
from flask import request
from flask_restx import Resource

from app.models.bookings import Appointment
from app.models.theq import CSR, CitizenState, PublicUser, Office, Service
from app.schemas.bookings import AppointmentSchema
from app.schemas.theq import CitizenSchema
from app.services import AvailabilityService
from app.utilities.auth_util import Role, get_username
from app.utilities.auth_util import is_public_user
from app.utilities.email import get_confirmation_email_contents, send_email, \
    get_blackout_email_contents
from app.utilities.snowplow import SnowPlow
from qsystem import api, api_call_with_retry, db, my_print, application
from qsystem import socketio
from app.auth.auth import jwt
from app.utilities.sms import send_sms


@api.route("/appointments/", methods=["POST"])
class AppointmentPost(Resource):
    appointment_schema = AppointmentSchema()
    citizen_schema = CitizenSchema()

    @api_call_with_retry
    @jwt.has_one_of_roles([Role.internal_user.value, Role.online_appointment_user.value])
    def post(self):
        my_print("==> In AppointmentPost, POST /appointments/")
        json_data = request.get_json()
        
        if not json_data:
            return {"message": "No input data received for creating an appointment"}, 400

        # Should delete draft appointment, and free up slot, before booking.
        # Clear up a draft if one was previously created by user reserving this time.
        if json_data.get('appointment_draft_id'):
            draft_id_to_delete = int(json_data['appointment_draft_id'])
            Appointment.delete_draft([draft_id_to_delete])
            if not application.config['DISABLE_AUTO_REFRESH']:
                socketio.emit('appointment_delete', draft_id_to_delete)
        #for stat
        if (json_data.get('stat_office_id', False)):
            json_data['office_id'] = json_data.get('stat_office_id')
        
        #get start date:
        start_time_ct = json_data.get('start_time', False)
        
        # remove below code, once code is tested - new req --> Stop blackouts from cancelling items (offices will call and cancel people individually if we have to close)
        is_blackout_appt = json_data.get('blackout_flag', 'N') == 'Y'
        csr = None
        user = None
        office = None

        #  Create a citizen for later use.
        citizen = self.citizen_schema.load({})

        # Check if the appointment is created by public user. Can't depend on the IDP as BCeID is used by other users as well
        is_public_user_appointment = is_public_user()
        if is_public_user_appointment:
            office_id = json_data.get('office_id')
            service_id = json_data.get('service_id')
            user = PublicUser.find_by_username(get_username())
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
                                                                      user_name=get_username(),
                                                                      start_time=json_data.get('start_time'),
                                                                      timezone=office.timezone.timezone_name)
            if appointments and len(appointments) >= office.max_person_appointment_per_day:
                return {"code": "MAX_NO_OF_APPOINTMENTS_REACHED",
                        "message": "Maximum number of appointments reached"}, 400

            # Check for race condition
            start_time = parse(json_data.get('start_time'))
            end_time = parse(json_data.get('end_time'))
            if not AvailabilityService.has_available_slots(office=office, start_time=start_time, end_time=end_time, service=service):
                return {"code": "CONFLICT_APPOINTMENT",
                        "message": "Cannot create appointment due to scheduling conflict.  Please pick another time."}, 400

        # elif (json_data.get('stat_flag', False)):
        #     #for stat
        #     csr = CSR.find_by_username(get_username())
        #     office_id = json_data.get('office_id', csr.office_id)
        #     office = Office.find_by_id(office_id)

        else:
            csr = CSR.find_by_username(get_username())
            office_id = json_data.get('office_id', csr.office_id)
            office = Office.find_by_id(office_id)

        citizen.office_id = office_id
        citizen.qt_xn_citizen_ind = 0
        citizen_state = CitizenState.query.filter_by(cs_state_name="Appointment booked").first()
        citizen.cs_id = citizen_state.cs_id
        citizen.start_time = start_time_ct
        citizen.service_count = 1
        db.session.add(citizen)
        db.session.commit()

        appointment = self.appointment_schema.load(json_data)
        warning = self.appointment_schema.validate(json_data)

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
            
            is_stat = (json_data.get('stat_flag', False))

            if ((not is_stat) and (not is_blackout_appt)):
                # Send confirmation email and sms
                try:
                    send_email(request.headers['Authorization'].replace('Bearer ', ''), *get_confirmation_email_contents(appointment, office, office.timezone, user))
                    send_sms(appointment, office, office.timezone, user,
                             request.headers['Authorization'].replace('Bearer ', ''))
                except Exception as exc:
                    logging.exception('Error on sms or email sending - %s', exc)

            SnowPlow.snowplow_appointment(citizen, csr, appointment, 'appointment_create')

            result = self.appointment_schema.dump(appointment)

            if not application.config['DISABLE_AUTO_REFRESH']:
                socketio.emit('appointment_create', result)

            return {"appointment": result,
                    "errors": {}}, 201

        else:
            return {"The Appointment Office ID and CSR Office ID do not match!"}, 403
