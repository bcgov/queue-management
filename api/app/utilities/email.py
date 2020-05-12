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

import pytz
from flask import current_app
from flask_mail import Mail
from flask_mail import Message
from jinja2 import Environment, FileSystemLoader

from app.models.bookings import Appointment

mail = Mail()  # pylint: disable=invalid-name
ENV = Environment(loader=FileSystemLoader('.'), autoescape=True)


def send_email(subject, email, sender, html_body):
    """Send the email asynchronously, using the given details."""

    if not email or not is_valid_email(email):
        print(f'Invalid email {email}. Skipping send.')
        return

    print('subject : ', subject)
    print('sender : ', sender)
    print('recipients : ', email)

    msg = Message(subject.encode('utf-8'), sender=sender, recipients=email.split())
    msg.html = html_body
    mail.send(msg)


def get_cancel_email_contents(appt: Appointment, user, office, timezone):
    """Send cancellation email"""
    sender = current_app.config.get('MAIL_FROM_ID')

    template = ENV.get_template('email_templates/delete_email.html')
    date = formatted_date(appt.start_time, timezone)
    subject = f'Cancelled – Your appointment on {date}'
    body = template.render(display_name=appt.citizen_name,
                           location=office.office_name,
                           formatted_date=date,
                           duration=get_duration(appt.start_time, appt.end_time),
                           telephone=office.telephone,
                           url=current_app.config.get('EMAIL_APPOINTMENT_APP_URL'))
    return subject, get_email(user, appt), sender, body


def get_reminder_email_contents(appt: Appointment, user, office, timezone):
    """Send cancellation email"""
    sender = current_app.config.get('MAIL_FROM_ID')

    template = ENV.get_template('email_templates/reminder_email.html')
    date = formatted_date(appt.start_time, timezone)
    subject = f'Reminder – Your appointment on {date}'
    body = template.render(display_name=appt.citizen_name,
                           location=office.office_name,
                           formatted_date=date,
                           duration=get_duration(appt.start_time, appt.end_time),
                           telephone=office.telephone,
                           url=current_app.config.get('EMAIL_APPOINTMENT_APP_URL'))
    return subject, get_email(user, appt), sender, body


def get_blackout_email_contents(blackout_appt: Appointment, cancelled_appointment: Appointment, office, timezone, user):
    """Send cancellation email"""
    sender = current_app.config.get('MAIL_FROM_ID')

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
    return subject, get_email(user, cancelled_appointment), sender, body


def get_confirmation_email_contents(appointment: Appointment, office, timezone, user):
    """Send confirmation email"""
    sender = current_app.config.get('MAIL_FROM_ID')

    template = ENV.get_template('email_templates/confirmation_email.html')
    date = formatted_date(appointment.start_time, timezone)
    subject = f'Confirmation – Your appointment on {date}'
    body = template.render(display_name=appointment.citizen_name,
                           location=office.office_name,
                           formatted_date=date,
                           duration=get_duration(appointment.start_time, appointment.end_time),
                           telephone=office.telephone,
                           url=current_app.config.get('EMAIL_APPOINTMENT_APP_URL'))
    return subject, get_email(user, appointment), sender, body


def is_valid_email(email: str):
    """Return if the email is valid or not."""
    return re.match(r'[^@]+@[^@]+\.[^@]+', email) is not None


def formatted_date(dt: datetime, timezone):
    dt_local = dt.astimezone(pytz.timezone(timezone.timezone_name))
    return dt_local.strftime('%B %d, %Y at %I:%M %p')


def get_duration(start_time: datetime, end_time: datetime):
    return int((end_time - start_time).total_seconds() / 60)


def get_email(user, appointment):
    return user.email if user else appointment.contact_information
