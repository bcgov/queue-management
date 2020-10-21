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
# from app.models.theq import CSR, CitizenState, PublicUser, Office, Service
from app.schemas.bookings import AppointmentSchema
# from app.schemas.theq import CitizenSchema
# from app.utilities.auth_util import Role, has_any_role
# from app.utilities.auth_util import is_public_user
# from app.utilities.date_util import add_delta_to_time
# from app.utilities.email import get_confirmation_email_contents, send_email, get_blackout_email_contents
# from app.utilities.snowplow import SnowPlow
from qsystem import api, api_call_with_retry, db, oidc, my_print
# from app.services import AvailabilityService
# from dateutil.parser import parse
# from pprint import pprint

from qsystem import socketio

# fetch("http://localhost:5000/api/v1/appointments/draft/flush", {
#   "headers": {
#     "accept": "application/json, text/plain, */*",
#     "accept-language": "en-US,en;q=0.9",
#   },
#   "body": "",
#   "method": "POST",
#   "mode": "cors",
#   "credentials": "include"
# });

@api.route("/appointments/draft/flush", methods=["POST"])
class AppointmentDraftFlush(Resource):

    # appointment_schema = AppointmentSchema()
    # Do weneed many=True here? is it causing crash?
    appointment_schema = AppointmentSchema(many=True)
    # citizen_schema = CitizenSchema()


    
    # Un-authenticated call as it can happen before user has logged in
    def post(self):
        # TODO - Require authentication with a specific token?
        my_print("==> In AppointmentDraftFlush, POST /appointments/draft/flush")

        drafts = Appointment.find_expired_drafts()
        appointments = Appointment.query.filter(Appointment.is_draft.is_(True))

        draft_result = self.appointment_schema.dump(drafts)
        appt_result = self.appointment_schema.dump(appointments)

        my_print('draft_result -- {}'.format(draft_result))
        my_print('appt_result -- {}'.format(appt_result))

        return {"drafts": draft_result.data, "drafts_unfiltered": appt_result.data}