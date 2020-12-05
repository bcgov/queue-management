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
from jinja2 import Environment, FileSystemLoader
import time
import jinja2, sys
from app.utilities.ches_email import send_email, generate_ches_token


setup_logging(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'logging.conf'))  # important to do this first


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

    send_reminders(application)


def send_reminders(app):
    """Send email reminders for next day appointments."""
    app.logger.debug('<<< Starting job')
    # CHES token
    ches_token = generate_ches_token()

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

            service_email_paragraph = appointment.service.email_paragraph
            if service_email_paragraph:
                service_email_paragraph = service_email_paragraph.replace('\r\n', '<br />')

            office_email_paragraph = appointment.office.office_email_paragraph
            if office_email_paragraph:
                office_email_paragraph = office_email_paragraph.replace('\r\n', '<br />')

            try:
                subject = 'Confirmation – Your appointment on {}'.format(appointment.get('day'))
                body = template.render(display_name=appointment.get('display_name'),
                                       location=appointment.get('location'),
                                       formatted_date=appointment.get('formatted_date'),
                                       duration=appointment.get('duration'),
                                       telephone=appointment.get('telephone'),
                                       service_name=appointment.service.external_service_name if appointment.service.external_service_name else appointment.service.service_name,
                                       civic_address=appointment.office.civic_address,
                                       url=app_url)
                send_email(ches_token, subject, appointment.get('email'), sender, body)
                email_count += 1

            except Exception as e:
                print(e)  # log and continue

            if email_count == max_email_per_batch:
                print('Pausing for a minute')
                time.sleep(60)
                email_count = 0
                # To handle token expiry, get a new token when the task resumes.
                ches_token = generate_ches_token()

    app.logger.debug('Ending job>>>')


if __name__ == "__main__":
    run()
