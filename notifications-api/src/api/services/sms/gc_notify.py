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

from notifications_python_client import NotificationsAPIClient

from . import SmsBaseService


class GCNotify(SmsBaseService):
    """Implementation from GC Notify."""

    def send(self, sms_payload):
        """Send SMS reminders for next day appointments."""
        api_key = os.getenv('GC_NOTIFY_API_KEY')
        gc_notify_url = os.getenv('GC_NOTIFY_API_BASE_URL')
        gc_template_id = os.getenv('GC_NOTIFY_SMS_TEMPLATE_ID')

        notifications_client = NotificationsAPIClient(api_key=api_key, base_url=gc_notify_url)
        sms_requests = sms_payload if type(sms_payload) == list else [sms_payload]

        for sms_request in sms_requests:
            try:
                if sms_request.get('user_telephone'):
                    sms_text = self._construct_sms_text(sms_request)

                    response = notifications_client.send_sms_notification(
                        phone_number=sms_request.get('user_telephone'),
                        template_id=gc_template_id,
                        personalisation={
                            'sms_text': sms_text
                        })
                    print(response)

            except Exception as e:
                print(e)  # log and continue

    @classmethod
    def _construct_sms_text(cls, sms_request: dict) -> str:
        """Construct SMS text."""
        message_type: str = sms_request.get('type', 'REMINDER')
        template: str = None
        app_url: str = os.getenv('APPOINTMENT_APP_URL')
        if message_type == 'REMINDER':
            template = os.getenv('SMS_REMINDER_TEMPLATE')
        elif message_type == 'CHECKIN_CONFIRMATION':
            template = os.getenv('SMS_CHECKIN_CONFIRMATION_TEMPLATE')
        elif message_type == 'CUSTOM':
            sms_text = sms_request.get('message')

        if template:
            sms_text = template.format(
                app_url=app_url,
                **sms_request
            )
        return sms_text
