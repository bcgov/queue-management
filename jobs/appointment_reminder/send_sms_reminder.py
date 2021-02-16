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
import json
import os

import requests
from flask import Flask

import config
from utils.appointment import get_reminders, get_access_token
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
    """Send SMS reminders for next day appointments."""
    app.logger.debug('<<< Starting job')

    reminders = get_reminders(app=app, reminder_type='sms')
    if reminders:
        appointments = reminders.json()
        notifications_endpoint = app.config.get('NOTIFICATIONS_ENDPOINT')
        token: str = get_access_token(app)
        notifications = []
        for appointment in appointments.get('appointments'):
            notifications.append({
                'user_telephone': appointment.get('user_telephone'),
                'display_name': appointment.get('display_name'),
                'location': appointment.get('location'),
                'formatted_date': appointment.get('formatted_date'),
                'office_telephone': appointment.get('telephone')
            })

        if notifications:
            try:
                response = requests.post(notifications_endpoint,
                                         headers={'Content-Type': 'application/json',
                                                  'Authorization': f'Bearer {token}'},
                                         data=json.dumps(notifications))
                print(response)
            except Exception as e:
                print(e)  # log and continue

    app.logger.debug('Ending job>>>')


if __name__ == "__main__":
    run()
