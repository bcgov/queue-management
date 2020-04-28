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

from threading import Thread

from flask import copy_current_request_context, current_app
from flask_mail import Mail
from flask_mail import Message

from app.models.bookings import Appointment
from app.models.theq import PublicUser, Citizen


mail = Mail()  # pylint: disable=invalid-name


def send_email(subject, sender, recipients, html_body):
    """Send the email, using the given details."""
    msg = Message(subject, sender=sender, recipients=recipients.split())
    msg.html = html_body
    mail.send(msg)


def async_email(subject, recipients, html_body):
    """Send the email asynchronously, using the given details."""

    sender = current_app.config.get('MAIL_FROM_ID')

    @copy_current_request_context
    def run_job():
        send_email(subject, sender, recipients, html_body)

    thread = Thread(target=run_job)
    thread.start()


def send_cancel_email(recipients):
    """Send cancellation email"""
    subject = 'Appointment Cancelled'
    body = 'Appointment Cancelled'
    async_email(subject, recipients, body)


def send_blackout_email(cancelled_appointments:[Appointment]):
    """Send cancellation email"""
    sender = current_app.config.get('MAIL_FROM_ID')

    # TODO Find all users with appointment and send email
    @copy_current_request_context
    def run_job():
        for appointment in cancelled_appointments:
            user: PublicUser = PublicUser.find_by_citizen_id(appointment.citizen_id)
            # if (user and user.email) or is_valid_email(appointment.contact_information):
            if user and user.email:
                send_email('Appointment Cancelled', sender, user.email, 'Appointment Cancelled')

    thread = Thread(target=run_job)
    thread.start()


# def is_valid_email():
#     """Return if email is valid"""
