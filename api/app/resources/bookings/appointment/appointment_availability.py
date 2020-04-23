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

from flask import g
from flask_restx import Resource
from qsystem import api, db, oidc
from sqlalchemy import exc
from app.models.theq import CSR, Office, TimeSlot
from app.schemas.theq import OfficeSchema
from app.models.bookings import Appointment
import json
from app.utilities.date_util import add_delta_to_time
import datetime, calendar, time
from datetime import timedelta
from dateutil import tz
import pytz


@api.route("/offices/<int:office_id>/slots/", methods=["GET"])
class OfficeSlots(Resource):

    @oidc.accept_token(require_token=False)
    def get(self, office_id: int):
        try:
            # find appointment duration per office and fetch timeslot master data
            appointment_duration = 30 #TODO get from config
            office = Office.find_by_id(office_id)
            appointments_days_limit = office.appointments_days_limit

            # Get all the dates from today until booking is allowed
            days = [datetime.datetime.now() + datetime.timedelta(days=x) for x in range(appointments_days_limit)]

            # Find all appointments between the dates
            appointments = Appointment.find_appointment_availability(office_id=office_id, first_date=days[0],
                                                                     last_date=days[-1])
            grouped_appointments = group_appointments(appointments, office.timezone.timezone_name)

            # Dictionary to store the available slots per day
            available_slots_per_day = {}

            # For each of the day calculate the slots based on time slots
            for day_in_month in days:
                formatted_date = day_in_month.strftime('%m/%d/%Y')
                available_slots_per_day[formatted_date] = []
                # TODO Check if day is stat holiday

                for timeslot in office.timeslots:
                    # Calculate the slots per day
                    if timeslot.day_of_week == day_in_month.weekday():
                        start_time = timeslot.start_time
                        end_time = add_delta_to_time(timeslot.start_time, delta=appointment_duration)

                        while end_time <= timeslot.end_time:
                            slot = {
                                'start_time': start_time,
                                'end_time': end_time,
                                'no_of_slots': timeslot.no_of_slots
                            }
                            available_slots_per_day[formatted_date].append(slot)
                            start_time = end_time
                            end_time = add_delta_to_time(end_time, delta=appointment_duration)

                # Check if the slots are already booked
                for actual_slot in available_slots_per_day[formatted_date]:
                    for booked_slot in grouped_appointments.get(formatted_date, []):

                        if actual_slot.get('start_time') <= booked_slot.get('start_time') < actual_slot.get(
                                'end_time') or \
                                actual_slot.get('start_time') < booked_slot.get('end_time') <= actual_slot.get(
                            'end_time'):
                            actual_slot['no_of_slots'] -= 1

                    actual_slot['start_time'] = actual_slot['start_time'].strftime('%H:%M')
                    actual_slot['end_time'] = actual_slot['end_time'].strftime('%H:%M')

            return available_slots_per_day

        except exc.SQLAlchemyError as e:
            print(e)
            return {'message': 'API is down'}, 500


def group_appointments(appointments, timezone:str):
    to_zone = 'America/Vancouver'
    filtered_appointments = {}
    for app in appointments:
        formatted_date = app.start_time.strftime('%m/%d/%Y')
        if not filtered_appointments.get(formatted_date, None):
            filtered_appointments[formatted_date] = []
        filtered_appointments[formatted_date].append({
            'start_time': app.start_time.astimezone(pytz.timezone(to_zone)).time(),
            'end_time': app.end_time.astimezone(pytz.timezone(to_zone)).time()
        })
    return filtered_appointments
