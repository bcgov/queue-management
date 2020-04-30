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

from flask import abort, g
from flask_restx import Resource

from app.models.bookings import Appointment
from app.utilities.auth_util import is_job
from app.utilities.email import send_reminder_email
from qsystem import api, api_call_with_retry, oidc


@api.route("/appointment/reminders/", methods=["POST"])
class AppointmentRemindersPost(Resource):

    @oidc.accept_token(require_token=True)
    @api_call_with_retry
    def post(self):
        """Create appointment reminders."""
        print('g.oidc_token_info-->', g.oidc_token_info)
        if not is_job():
            abort(403)

        appointments = Appointment.find_next_day_appointments()

        print(appointments)
        if appointments:
            for (appointment, office, timezone, user) in appointments:
                send_reminder_email(appointment, user, office, timezone)
