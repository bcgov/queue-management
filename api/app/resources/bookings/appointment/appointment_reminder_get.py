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

from flask_restx import Resource

from app.models.bookings import Appointment
from app.utilities.auth_util import Role, has_any_role
from app.utilities.email import is_valid_email, formatted_date, get_email, \
    get_duration
from qsystem import api, api_call_with_retry, oidc


@api.route("/appointment/reminders/", methods=["GET"])
class AppointmentRemindersGet(Resource):

    @oidc.accept_token(require_token=True)
    @api_call_with_retry
    @has_any_role(roles=[Role.reminder_job.value])
    def get(self):
        """Return appointment reminders for next day."""
        appointments = Appointment.find_next_day_appointments()

        # Construct a custom response as teh payload can grow in size.
        reminders = {
            'appointments': []
        }

        if appointments:
            for (appointment, office, timezone, user) in appointments:
                send_reminder = False
                if user and user.send_reminders:
                    send_reminder = True
                elif not user and is_valid_email(appointment.contact_information):
                    send_reminder = True

                if send_reminder:
                    date, day = formatted_date(appointment.start_time, timezone)

                    reminders['appointments'].append(
                        {
                            'formatted_date': date,
                            'day': day,
                            'email': get_email(user, appointment),
                            'display_name': appointment.citizen_name,
                            'location': office.office_name,
                            'duration': get_duration(appointment.start_time, appointment.end_time),
                            'telephone': office.telephone
                        }
                    )
        return reminders
