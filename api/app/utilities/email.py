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

import re
from datetime import datetime
from threading import Thread

import pytz
from flask import copy_current_request_context, current_app
from flask_mail import Mail
from flask_mail import Message
from jinja2 import Environment, FileSystemLoader

from app.models.bookings import Appointment
from app.models.theq import PublicUser

mail = Mail()  # pylint: disable=invalid-name
ENV = Environment(loader=FileSystemLoader('.'), autoescape=True)


def async_email(subject, appt: Appointment, user: PublicUser, html_body):
    """Send the email asynchronously, using the given details."""

    sender = current_app.config.get('MAIL_FROM_ID')

    @copy_current_request_context
    def run_job():
        email = user.email if user else appt.contact_information
        if not is_valid_email(email):
            print(f'Invalid email {email}. Skipping send.')
            return
        print('subject : ', subject)
        print('sender : ', sender)
        print('recipients : ', email)
        print('html_body : ', html_body)

        msg = Message(subject, sender=sender, recipients=email.split())
        msg.html = html_body
        mail.send(msg)

    thread = Thread(target=run_job)
    thread.start()


def send_cancel_email(appt: Appointment, user, office, timezone):
    """Send cancellation email"""
    template = ENV.get_template('email_templates/delete_email.html')
    date = formatted_date(appt.start_time, timezone)
    subject = f'Cancelled – Your appointment on {date}'
    body = template.render(display_name=appt.citizen_name,
                           location=office.office_name,
                           formatted_date=date,
                           duration=get_duration(appt.start_time, appt.end_time),
                           telephone=office.telephone,
                           url=current_app.config.get('EMAIL_APPOINTMENT_APP_URL'))
    async_email(subject, appt, user, body)


def send_reminder_email(appt: Appointment, user, office, timezone):
    """Send cancellation email"""
    template = ENV.get_template('email_templates/reminder_email.html')
    date = formatted_date(appt.start_time, timezone)
    subject = f'Reminder – Your appointment on {date}'
    body = template.render(display_name=appt.citizen_name,
                           location=office.office_name,
                           formatted_date=date,
                           duration=get_duration(appt.start_time, appt.end_time),
                           telephone=office.telephone,
                           url=current_app.config.get('EMAIL_APPOINTMENT_APP_URL'))
    async_email(subject, appt, user, body)


def send_blackout_email(blackout_appt: Appointment, cancelled_appointment: Appointment, office, timezone, user):
    """Send cancellation email"""
    template = ENV.get_template('email_templates/blackout_email.html')
    date = formatted_date(cancelled_appointment.start_time, timezone)
    subject = f'Cancelled – Your appointment on {date}'
    body = template.render(display_name=cancelled_appointment.citizen_name,
                           location=office.office_name,
                           formatted_date=date,
                           duration=get_duration(cancelled_appointment.start_time, cancelled_appointment.end_time),
                           telephone=office.telephone,
                           url=current_app.config.get('EMAIL_APPOINTMENT_APP_URL'),
                           blackout_notes=blackout_appt.comments)
    async_email(subject, cancelled_appointment, user, body)


def is_valid_email(email: str):
    """Return if the email is valid or not."""
    return re.match(r'[^@]+@[^@]+\.[^@]+', email) is not None


def formatted_date(dt: datetime, timezone):
    dt_local = dt.astimezone(pytz.timezone(timezone.timezone_name))
    return dt_local.strftime('%Y-%m-%d at %I:%M %p')


def get_duration(start_time: datetime, end_time: datetime):
    return int((end_time - start_time).total_seconds() / 60)
