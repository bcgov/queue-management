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

from dateutil.parser import parse
from flask import request, g
from flask_restx import Resource

from app.models.bookings import Appointment
from app.models.theq import CSR, PublicUser, Office, Service
from app.schemas.bookings import AppointmentSchema
from app.schemas.theq import CitizenSchema
from app.services import AvailabilityService
from app.utilities.auth_util import get_username
from app.utilities.date_util import add_delta_to_time
from qsystem import api, db, my_print, application
from qsystem import socketio


@api.route("/appointments/draft", methods=["POST"])
class AppointmentDraftPost(Resource):
    appointment_schema = AppointmentSchema()
    citizen_schema = CitizenSchema()

    # Un-authenticated call as it can happen before user has logged in    
    def post(self):
        my_print("==> In AppointmentDraftPost, POST /appointments/draft")
        json_data = request.get_json()

        office_id = json_data.get('office_id')
        service_id = json_data.get('service_id')
        start_time = parse(json_data.get('start_time'))
        end_time = parse(json_data.get('end_time'))
        office = Office.find_by_id(office_id)
        service = Service.query.get(int(service_id)) if service_id else None

        # end_time can be null for CSRs when they click; whereas citizens know end-time.
        if not end_time:
            end_time = add_delta_to_time(start_time, minutes=office.appointment_duration, timezone=office.timezone.timezone_name)

        # Unauthenticated requests from citizens won't have name, so we set a fallback
        if (hasattr(g, 'jwt_oidc_token_info') and hasattr(g.jwt_oidc_token_info, 'username')):
            user = PublicUser.find_by_username(get_username())
            citizen_name = user.display_name
        else:
            citizen_name = 'Draft'

        # Delete all expired drafts before checking availability
        Appointment.delete_expired_drafts()

        csr = None
        if (hasattr(g, 'jwt_oidc_token_info')):
            csr = CSR.find_by_username(get_username())

        # CSRs are not limited by drafts,  can always see other CSRs drafts
        # This mitigates two CSRs in office creating at same time for same meeting
        # Ensure there's no race condition when submitting a draft
        if not csr and not AvailabilityService.has_available_slots(
                                    office=office,
                                    start_time=start_time,
                                    end_time=end_time,
                                    service=service):
                                return {"code": "CONFLICT_APPOINTMENT",
                                        "message": "Cannot create appointment due to scheduling conflict.  Please pick another time."}, 400

        # Set draft specific data
        json_data['is_draft'] = True
        json_data['citizen_name'] = citizen_name

        warning = self.appointment_schema.validate(json_data)
        appointment = self.appointment_schema.load(json_data)

        if warning:
            logging.warning("WARNING: %s", warning)
            return {"message": warning}, 422

        db.session.add(appointment)
        db.session.commit()

        result = self.appointment_schema.dump(appointment)

        if not application.config['DISABLE_AUTO_REFRESH']:
            socketio.emit('appointment_create', result)

        return {"appointment": result, "warning": warning}, 201
