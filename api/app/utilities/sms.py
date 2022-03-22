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
from pprint import pprint

import json
import pytz
import requests
from flask import current_app

from app.models.bookings import Appointment
from app.models.theq import Office, PublicUser, Citizen

# Defining String constants to appease SonarQube
app_json_const = 'application/json'

def send_sms(appointment: Appointment, office: Office, timezone, user: PublicUser, token: str):
    """Send confirmation email"""
    telephone: str = get_user_telephone(user, appointment)
    if telephone:
        notifications_endpoint = current_app.config.get('NOTIFICATIONS_ENDPOINT')
        try:
            display_name: str = user.display_name if user else ''  # For CSR appointment user is None
            requests.post(notifications_endpoint,
                          headers={'Content-Type': app_json_const, 'Authorization': f'Bearer {token}'},
                          data=json.dumps([{
                              'user_telephone': telephone,
                              'display_name': display_name,
                              'location': office.office_name,
                              'formatted_date': format_sms_date(appointment.start_time, timezone),
                              'office_telephone': office.telephone
                          }]))
        except Exception as exc:
            pprint(f'Error on sms sending - {exc}')


def is_valid_phone(phone_number: str):
    """Return if the phone_number is valid or not."""
    if phone_number:
        phone_number = phone_number.replace(' ', '').replace('(', '').replace(')', '')
        # Redoing this phone number regex which is unnecessarily complex.
        # It strips spaces and () but then checked for them (?) and also accepted 7 digit numbers (?)
        return re.match(r'\+?1?[-\.]?\d{3}[-\.]?\d{3}[-\.]?\d{4}', phone_number) is not None
    return False


def format_sms_date(dt: datetime, timezone):
    dt_local = dt.astimezone(pytz.timezone(timezone.timezone_name))
    return dt_local.strftime('%A, %B %d at %I:%M %p')


def get_user_telephone(user, appointment):
    if user:
        phone = user.telephone if user.send_sms_reminders else None
    else:
        phone = appointment.contact_information if is_valid_phone(appointment.contact_information) else None
    return phone


def send_walkin_spot_confirmation_sms(citizen: Citizen, url, token: str):
    """Send walkin spot confirmation email"""
    telephone: str = citizen.notification_phone
    if telephone:
        notifications_endpoint = current_app.config.get('NOTIFICATIONS_ENDPOINT')
        try:
            requests.post(notifications_endpoint,
                          headers={'Content-Type': app_json_const, 'Authorization': f'Bearer {token}'},
                          data=json.dumps([{
                              'user_telephone': telephone,
                              'url': url,
                              'ticket_number': citizen.ticket_number,
                              "type": "CHECKIN_CONFIRMATION"
                        }]))
            return True
        except Exception as exc:
            pprint(f'Error on sms sending - {exc}')
            return False
    return False


def send_walkin_reminder_sms(citizen: Citizen, office: Office, token: str):
    """Send walkin spot confirmation email"""
    telephone: str = citizen.notification_phone
    if telephone:
        notifications_endpoint = current_app.config.get('NOTIFICATIONS_ENDPOINT')
        try:
            msg = "We’re ready! Please come inside and speak to a Service BC Representative"
            requests.post(notifications_endpoint,
                          headers={'Content-Type': app_json_const, 'Authorization': f'Bearer {token}'},
                          data=json.dumps([{
                              'user_telephone': telephone,
                              'message': office.check_in_reminder_msg if office.check_in_reminder_msg else msg,
                              "type": "CUSTOM"
                          }]))
            return True
        except Exception as exc:
            pprint(f'Error on sms sending - {exc}')
            return False
    return False
