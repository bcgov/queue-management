# Copyright © 2019 Province of British Columbia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Send SMS reminder.

This module is being invoked from a job and it sends SMS reminders to customers.
"""
import os
from typing import Dict

from notifications_python_client import NotificationsAPIClient

from utils.logging import setup_logging
from . import SmsBaseService

setup_logging(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'logging.conf'))  # important to do this first


class GCNotify(SmsBaseService):
    """Implementation from GC Notify."""

    def send(self, app: any, reminders: Dict):
        """Send SMS reminders for next day appointments."""
        api_key = app.config.get('GC_NOTIFY_API_KEY')
        gc_notify_url = app.config.get('GC_NOTIFY_API_BASE_URL')
        gc_template_id = app.config.get('GC_NOTIFY_SMS_TEMPLATE_ID')
        app_url = app.config.get('EMAIL_APPOINTMENT_APP_URL')

        notifications_client = NotificationsAPIClient(api_key=api_key, base_url=gc_notify_url)

        for appointment in reminders.get('appointments'):
            try:
                if appointment.get('user_telephone'):
                    response = notifications_client.send_sms_notification(
                        phone_number=appointment.get('user_telephone'),
                        template_id=gc_template_id,
                        personalisation={
                            'location': appointment.get('location'),
                            'duration': appointment.get('duration'),
                            'formatted_date': appointment.get('formatted_date'),
                            'app_url': app_url,
                            'display_name': appointment.get('display_name')
                        })
                    print(response)

            except Exception as e:
                print(e)  # log and continue
