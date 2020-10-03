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
"""The Update Payment Job.

This module is being invoked from a job and it cleans up the stale records
"""
import os

import base64
import requests
from flask import Flask

import config
from utils.logging import setup_logging
from flask_mail import Mail
from flask_mail import Message
from jinja2 import Environment, FileSystemLoader
import time
import jinja2, sys

setup_logging(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'logging.conf'))  # important to do this first

mail = Mail()  # pylint: disable=invalid-name


def create_app(run_mode=os.getenv('FLASK_ENV', 'production')):
    """Return a configured Flask App using the Factory method."""
    app = Flask(__name__)

    app.config.from_object(config.CONFIGURATION[run_mode])

    register_shellcontext(app)

    return app


def register_shellcontext(app):
    """Register shell context objects."""

    def shell_context():
        """Shell context objects."""
        return {
            'app': app
        }

    app.shell_context_processor(shell_context)


def run():
    application = create_app()
    application.app_context().push()
    mail.init_app(application)

    send_reminders(application)


def send_reminders(app):
    """Send email reminders for next day appointments."""
    app.logger.debug('<<< Starting job')

    # Create a keycloak service account token to call the appointment api
    token_url = app.config.get('OIDC_PROVIDER_TOKEN_URL')  # https://sso-dev.pathfinder.gov.bc.ca/auth/realms/fcf0kpqr/protocol/openid-connect/token
    basic_auth_encoded = base64.b64encode(
        bytes(app.config.get('SERVICE_ACCOUNT_ID') + ':' + app.config.get('SERVICE_ACCOUNT_SECRET'), 'utf-8')).decode(
        'utf-8')
    data = 'grant_type=client_credentials'
    headers = {
        'Authorization': f'Basic {basic_auth_encoded}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    token_response = requests.post(token_url, data=data, headers=headers)
    # print(token_response.json())
    access_token = token_response.json().get('access_token')

    # Add this token as bearer token to invoke the reminders endpoint
    reminders_endpoint = app.config.get('REMINDER_ENDPOINT')
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    # response = requests.post(reminders_endpoint, data=None, headers=headers)
    response = requests.get(reminders_endpoint, data=None, headers=headers)
    response.raise_for_status()

    if response:
        sender = app.config.get('MAIL_FROM_ID')
        app_url = app.config.get('EMAIL_APPOINTMENT_APP_URL')
        app_folder = [folder for folder in sys.path if 'api/api' in folder][0]
        template_path = app_folder.replace('api/api', 'api/api/email_templates')
        env = Environment(loader=FileSystemLoader(template_path), autoescape=True)
        template = env.get_template('confirmation_email.html')
        max_email_per_batch = app.config.get('MAX_EMAIL_PER_BATCH')
        print(f'Maximum email per batch {max_email_per_batch}')

        appointments = response.json()
        email_count = 0
        print('found {} reminders to send!'.format(len(appointments.get('appointments'))))

        for appointment in appointments.get('appointments'):
            try:
                subject = 'Confirmation – Your appointment on {}'.format(appointment.get('day'))
                body = template.render(display_name=appointment.get('display_name'),
                                       location=appointment.get('location'),
                                       formatted_date=appointment.get('formatted_date'),
                                       duration=appointment.get('duration'),
                                       telephone=appointment.get('telephone'),
                                       url=app_url)
                msg = Message(subject, sender=sender, recipients=appointment.get('email').split())
                msg.html = body
                mail.send(msg)
                email_count += 1
            except Exception as e:
                print(e) #log and continue

            print('Pausing for a minute')
            if email_count == max_email_per_batch:
                time.sleep(60)
                email_count = 0

    app.logger.debug('Ending job>>>')


if __name__ == "__main__":
    run()
