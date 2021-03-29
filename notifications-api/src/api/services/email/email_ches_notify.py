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
import os, json, requests
from notifications_python_client import NotificationsAPIClient

from . import EmailBaseService


class EmailChesNotify(EmailBaseService):
    """Implementation from Ches Email Notify."""

    def send(self, email_payload):
        """Send SMS reminders for next day appointments."""
        ches_token_url = os.getenv('CHES_SSO_TOKEN_URL')
        ches_client_id = os.getenv('CHES_SSO_CLIENT_ID')
        ches_client_secret = os.getenv('CHES_SSO_CLIENT_SECRET')
        ches_email_endpoint = os.getenv('CHES_POST_EMAIL_ENDPOINT')
        ches_payload = {
            'bodyType': email_payload.get('bodyType'),
            'body': email_payload.get('body'),
            'from': os.getenv('CHES_EMAIL_FROM_ID'),
            'subject': email_payload.get('subject'),
            'to': email_payload.get('to')
        }
        try:
            ches_token_response = requests.post(ches_token_url,
                                    data=f'client_id={ches_client_id}&client_secret={ches_client_secret}&grant_type=client_credentials',
                                    headers={'Content-Type': 'application/x-www-form-urlencoded'})
            ches_api_token = ches_token_response.json().get('access_token')
            email_response = requests.post(ches_email_endpoint,
                                headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {ches_api_token}'},
                                data=json.dumps(ches_payload))
            print(email_response)
        except Exception as e:
            print(e)  # log and continue
