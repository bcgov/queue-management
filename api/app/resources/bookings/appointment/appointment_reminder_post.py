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

from threading import Thread

from flask import copy_current_request_context, current_app
from flask_restx import Resource

from app.models.bookings import Appointment
from app.utilities.auth_util import Role, has_any_role
from app.utilities.email import get_reminder_email_contents, send_email
from qsystem import api, api_call_with_retry, oidc


@api.route("/appointment/reminders/", methods=["POST"])
class AppointmentRemindersPost(Resource):

    @oidc.accept_token(require_token=True)
    @api_call_with_retry
    @has_any_role(roles=[Role.reminder_job.value])
    def post(self):
        """Create appointment reminders."""
        appointments = Appointment.find_next_day_appointments()
        print('sending {} reminders'.format(len(appointments)))

        if appointments:
            for (appointment, office, timezone, user) in appointments:
                if user.send_reminders:
                    @copy_current_request_context
                    def async_email(subject, email, sender, body):
                        send_email(subject, email, sender, body)

                    thread = Thread(target=async_email, args=get_reminder_email_contents(appointment, user, office, timezone))
                    thread.start()
