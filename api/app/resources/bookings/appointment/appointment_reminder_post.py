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
from app.utilities.email import get_reminder_email_contents, send_email, is_valid_email
from qsystem import api, api_call_with_retry, oidc


@api.route("/appointment/reminders/", methods=["POST"])
class AppointmentRemindersPost(Resource):

    @oidc.accept_token(require_token=True)
    @api_call_with_retry
    @has_any_role(roles=[Role.reminder_job.value])
    def post(self):
        """Create appointment reminders."""
        appointments = Appointment.find_next_day_appointments()

        reminder_count: int = 0
        if appointments:
            for (appointment, office, timezone, user) in appointments:
                send_reminder = False
                if user and user.send_reminders:
                    send_reminder = True
                elif not user and is_valid_email(appointment.contact_information):
                    send_reminder = True

                if send_reminder:
                    @copy_current_request_context
                    def async_email(subject, email, sender, body):
                        send_email(subject, email, sender, body)

                    reminder_count += 1
                    thread = Thread(target=async_email, args=get_reminder_email_contents(appointment, user, office, timezone))
                    thread.daemon = True
                    thread.start()

        print(f'Sending {reminder_count} reminders')
