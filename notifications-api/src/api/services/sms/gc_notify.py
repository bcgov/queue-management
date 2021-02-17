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
        app_url = os.getenv('APPOINTMENT_APP_URL')

        notifications_client = NotificationsAPIClient(api_key=api_key, base_url=gc_notify_url)
        sms_requests = sms_payload if type(sms_payload) == list else [sms_payload]

        for sms_request in sms_requests:
            try:
                if sms_request.get('user_telephone'):
                    sms_text = os.getenv('SMS_REMINDER_TEMPLATE').format(
                        first_name=sms_request.get('display_name'),
                        location=sms_request.get('location'),
                        date_time=sms_request.get('formatted_date'),
                        app_url=app_url,
                        office_telephone=sms_request.get('office_telephone')
                    )

                    response = notifications_client.send_sms_notification(
                        phone_number=sms_request.get('user_telephone'),
                        template_id=gc_template_id,
                        personalisation={
                            'sms_text': sms_text
                        })
                    print(response)

            except Exception as e:
                print(e)  # log and continue
