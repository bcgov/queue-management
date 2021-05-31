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

import json
import re

import requests
from flask import current_app


def send_email(token, subject, email, sender, html_body):
    """Send the email asynchronously, using the given details."""
    if not email or not is_valid_email(email):
        return

    send_email_endpoint = current_app.config.get('NOTIFICATIONS_EMAIL_ENDPOINT')
    payload = {
        'bodyType': 'text',
        'body': html_body,
        'from': sender,
        'subject': subject,
        'to': email.split()
    }
    response = requests.post(send_email_endpoint,
                             headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'},
                             data=json.dumps(payload))
    response.raise_for_status()


def is_valid_email(email: str):
    """Return if the email is valid or not."""
    if email:
        return re.match(r'[^@]+@[^@]+\.[^@]+', email) is not None
    return False
