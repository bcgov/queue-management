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
from app.schemas.bookings import AppointmentSchema
from qsystem import api, api_call_with_retry, db, oidc, my_print

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

    appointment_schema = AppointmentSchema(many=True)
    
    # Un-authenticated call as it can happen before user has logged in
    def post(self):
        # TODO - Require authentication with a specific token?
        # TODO - Potentialy move into cron job, call Sumesh to discuss
        my_print("==> In AppointmentDraftFlush, POST /appointments/draft/flush")
        drafts = Appointment.find_expired_drafts()
        draft_ids = [appointment.appointment_id for appointment in drafts]
        my_print('==> Deleting draft appointments with ids: {}'.format(draft_ids))
        Appointment.delete_appointments(draft_ids)
        return {"deleted_draft_ids": draft_ids}, 200