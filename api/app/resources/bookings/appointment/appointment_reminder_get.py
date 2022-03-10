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
from qsystem import api, api_call_with_retry
from app.auth.auth import jwt
from app.utilities.sms import is_valid_phone, format_sms_date


@api.route("/appointment/reminders/<string:reminder_type>/", methods=["GET"])
class AppointmentRemindersGet(Resource):

    @api_call_with_retry
    @jwt.has_one_of_roles([Role.reminder_job.value])
    def get(self, reminder_type: str = 'email'):
        """Return appointment reminders for next day."""
        appointments = Appointment.find_next_day_appointments()

        # Construct a custom response as teh payload can grow in size.
        reminders = {
            'appointments': []
        }

        if appointments:
            for (appointment, office, timezone, user) in appointments:
                send_reminder = False
                user_telephone = None
                if reminder_type == 'email':
                    if (user and user.send_email_reminders) or (not user and is_valid_email(appointment.contact_information)):
                        send_reminder = True
                elif reminder_type == 'sms':
                    if user and user.send_sms_reminders:
                        send_reminder = True
                        user_telephone = user.telephone
                    elif not user and is_valid_phone(appointment.contact_information):
                        send_reminder = True
                        user_telephone = appointment.contact_information

                if send_reminder:
                    if reminder_type == 'email':
                        date, day = formatted_date(appointment.start_time, timezone)
                    else:
                        date, day = format_sms_date(appointment.start_time, timezone), None

                    office_email_paragraph = appointment.office.office_email_paragraph

                    service_email_paragraph = appointment.service.email_paragraph

                    service_name = appointment.service.external_service_name \
                        if appointment.service.external_service_name else appointment.service.service_name

                    reminders['appointments'].append(
                        {
                            'formatted_date': date,
                            'day': day,
                            'email': get_email(user, appointment),
                            'display_name': appointment.citizen_name,
                            'location': office.office_name,
                            'duration': get_duration(appointment.start_time, appointment.end_time),
                            'telephone': office.telephone,
                            'service_email_paragraph': service_email_paragraph,
                            'office_email_paragraph': office_email_paragraph,
                            'service_name': service_name,
                            'civic_address': appointment.office.civic_address,
                            'user_telephone': user_telephone,
                        }
                    )
        return reminders
