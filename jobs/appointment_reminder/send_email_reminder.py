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
"""The Send email reminders job.

This module is being invoked from a job and it cleans up the stale records
"""
import os

import sys
import time
from app.utilities.notification_email import send_email
from utils.appointment import get_reminders, get_access_token
from flask import Flask
from jinja2 import Environment, FileSystemLoader

import config
from utils.appointment import get_reminders
from utils.logging import setup_logging

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
    # ACCESS token
    access_token = get_access_token(app)

    reminders = get_reminders(app=app)

    if reminders:
        sender = app.config.get('MAIL_FROM_ID')
        app_url = app.config.get('EMAIL_APPOINTMENT_APP_URL')
        app_folder = [folder for folder in sys.path if 'api/api' in folder][0]
        template_path = app_folder.replace('api/api', 'api/api/email_templates')
        env = Environment(loader=FileSystemLoader(template_path), autoescape=True)
        template = env.get_template('confirmation_email.html')
        max_email_per_batch = app.config.get('MAX_EMAIL_PER_BATCH')
        print(f'Maximum email per batch {max_email_per_batch}')

        appointments = reminders.json()
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
                                       service_name=appointment.get('service_name'),
                                       civic_address=appointment.get('civic_address'),
                                       service_email_paragraph=appointment.get('service_email_paragraph'),
                                       office_email_paragraph=appointment.get('office_email_paragraph'),
                                       url=app_url)
                send_email(access_token, subject, appointment.get('email'), sender, body)
                email_count += 1

            except Exception as e:
                print(e)  # log and continue

            if email_count == max_email_per_batch:
                print('Pausing for a minute')
                time.sleep(60)
                email_count = 0
                # To handle token expiry, get a new token when the task resumes.
                access_token = get_access_token(app)

    app.logger.debug('Ending job>>>')


if __name__ == "__main__":
    run()
