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

import datetime
from typing import Dict

import pytz
from flask_restx import Resource
from sqlalchemy import exc

from app.models.bookings import Appointment
from app.models.theq import Office
from app.utilities.date_util import add_delta_to_time, day_indexes
from qsystem import api, oidc


@api.route("/offices/<int:office_id>/slots/", methods=["GET"])
class OfficeSlots(Resource):

    @oidc.accept_token(require_token=False)
    def get(self, office_id: int):
        try:
            available_slots_per_day = {}
            office = Office.find_by_id(office_id)
            if office.appointments_enabled_ind == 0:
                return available_slots_per_day

            # find appointment duration per office and fetch timeslot master data
            appointment_duration = office.appointment_duration
            appointments_days_limit = office.appointments_days_limit

            # Get all the dates from today until booking is allowed
            days = [datetime.datetime.now() + datetime.timedelta(days=x) for x in range(appointments_days_limit)]

            # Find all appointments between the dates
            appointments = Appointment.find_appointment_availability(office_id=office_id, first_date=days[0],
                                                                     last_date=days[-1], timezone=office.timezone.timezone_name)
            grouped_appointments = group_appointments(appointments, office.timezone.timezone_name)

            # Dictionary to store the available slots per day

            # For each of the day calculate the slots based on time slots
            for day_in_month in days:
                formatted_date = day_in_month.strftime('%m/%d/%Y')
                available_slots_per_day[formatted_date] = []

                for timeslot in office.timeslots:
                    # Calculate the slots per day
                    if day_in_month.isoweekday() in day_indexes(timeslot.day_of_week):
                        start_time = timeslot.start_time.replace(tzinfo=pytz.timezone(office.timezone.timezone_name))
                        end_time = add_delta_to_time(timeslot.start_time, minutes=appointment_duration, timezone=office.timezone.timezone_name)
                        # print(start_time, end_time)
                        while end_time <= timeslot.end_time:
                            slot = {
                                'start_time': start_time,
                                'end_time': end_time,
                                'no_of_slots': timeslot.no_of_slots
                            }
                            available_slots_per_day[formatted_date].append(slot)
                            start_time = end_time.replace(tzinfo=pytz.timezone(office.timezone.timezone_name))
                            end_time = add_delta_to_time(end_time, minutes=appointment_duration, timezone=office.timezone.timezone_name)

                # Check if the slots are already booked
                for actual_slot in available_slots_per_day[formatted_date]:
                    for booked_slot in grouped_appointments.get(formatted_date, []):
                        # print('>>>>>>', booked_slot.get('start_time'), actual_slot.get('start_time'), booked_slot.get('end_time'))
                        # print('<<<<<<', booked_slot.get('end_time'), actual_slot.get('end_time'),
                        #       booked_slot.get('start_time'))

                        if booked_slot.get('start_time') \
                                <= actual_slot.get('start_time') \
                                < booked_slot.get('end_time') \
                                or \
                                booked_slot.get('end_time') \
                                < actual_slot.get('end_time') \
                                <= booked_slot.get('start_time'):
                            if booked_slot.get('blackout_flag', False):  # If it's blackout override the no of slots
                                actual_slot['no_of_slots'] = 0
                            else:
                                actual_slot['no_of_slots'] -= 1

                    actual_slot['start_time'] = actual_slot['start_time'].strftime('%H:%M')
                    actual_slot['end_time'] = actual_slot['end_time'].strftime('%H:%M')

            return prune_appointments(available_slots_per_day)

        except exc.SQLAlchemyError as e:
            print(e)
            return {'message': 'API is down'}, 500


def group_appointments(appointments, timezone: str):
    filtered_appointments = {}
    for app in appointments:
        formatted_date = app.start_time.strftime('%m/%d/%Y')
        if not filtered_appointments.get(formatted_date, None):
            filtered_appointments[formatted_date] = []
        # print('app.blackout_flag', app.blackout_flag)
        filtered_appointments[formatted_date].append({
            'start_time': app.start_time.astimezone(pytz.timezone(timezone)).time(),
            'end_time': app.end_time.astimezone(pytz.timezone(timezone)).time(),
            'blackout_flag': app.blackout_flag == 'Y'
        })
    return filtered_appointments


def prune_appointments(available_slots_per_day: Dict):
    for key, slots in available_slots_per_day.items():
        for slot in reversed(slots):
            if slot['no_of_slots'] <= 0:
                slots.remove(slot)

    return available_slots_per_day
