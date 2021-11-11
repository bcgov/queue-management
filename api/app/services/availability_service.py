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
from sqlalchemy import exc

from app.models.bookings import Appointment
from app.models.theq import Office
from app.models.theq import Service
from app.utilities.date_util import add_delta_to_time, day_indexes
from app.utilities.yesno import YesNo


class AvailabilityService():

    @staticmethod
    def get_available_slots(office: Office, days: [datetime], format_time: bool = True, service: Service = None):
        """Return the available slots for the office"""
        try:
            available_slots_per_day = {}
            if office.appointments_enabled_ind == 0:
                return available_slots_per_day

            # find appointment duration per office and fetch timeslot master data
            appointment_duration = office.appointment_duration

            # If user has passed in service and it has duration, use that instead
            if (service and service.timeslot_duration):
                appointment_duration = service.timeslot_duration

            service_is_dltk = service and service.is_dlkt == YesNo.YES
            
            # Dictionary to store the available slots per day
            tz = pytz.timezone(office.timezone.timezone_name)

            # today's date and time
            today = datetime.datetime.now().astimezone(tz)

            # soonest a citizen can book an appointment
            soonest_appointment_date = today + datetime.timedelta(minutes = office.soonest_appointment or 0)

            # Find all appointments between the dates
            appointments = Appointment.find_appointment_availability(office_id=office.office_id, first_date=today,
                                                                     last_date=days[-1],
                                                                     timezone=office.timezone.timezone_name)
            grouped_appointments = AvailabilityService.group_appointments(appointments, office.timezone.timezone_name)

            # For each of the day calculate the slots based on time slots
            for day_in_month in days:
                formatted_date = day_in_month.strftime('%m/%d/%Y')
                available_slots_per_day[formatted_date] = []
                for timeslot in office.timeslots:
                    # Calculate the slots per day
                    timeslot_end_time = timeslot.end_time.replace(tzinfo=tz)
                    timeslot_start_time = timeslot.start_time.replace(tzinfo=tz)
                    if day_in_month.isoweekday() in day_indexes(timeslot.day_of_week):
                        start_time = timeslot_start_time
                        end_time = add_delta_to_time(timeslot_start_time, minutes=appointment_duration,
                                                     timezone=office.timezone.timezone_name)
                        # print(start_time, end_time)

                        # Cannot exceed office timeslot slots.
                        dlkt_slots = office.number_of_dlkt  or 0
    
                        if ( dlkt_slots > timeslot.no_of_slots):
                            dlkt_slots = timeslot.no_of_slots
                        

                        # Limit DLKT slots only for DLKT services.
                        # no_of_slots = dlkt_slots if service_is_dltk else timeslot.no_of_slots
                        no_of_slots = timeslot.no_of_slots

                        while end_time <= timeslot_end_time:
                            slot = {
                                'start_time': start_time,
                                'end_time': end_time,
                                'no_of_slots': no_of_slots,
                                'no_of_dlkt_slots': dlkt_slots
                            }
                            # Check if today's time is past appointment slot
                            # Arc - also check if in office.soonest_appointment
                            if not (today.date() == day_in_month.date() and start_time > soonest_appointment_date.time()):
                                if slot not in available_slots_per_day[formatted_date]: 
                                    available_slots_per_day[formatted_date].append(slot)

                            start_time = end_time.replace(tzinfo=tz)
                            end_time = add_delta_to_time(end_time, minutes=appointment_duration,
                                                         timezone=office.timezone.timezone_name)

                # Sort the slot by time for the day
                available_slots_per_day[formatted_date].sort(key=lambda x: x['start_time'])

                # Check if the slots are already booked
                for actual_slot in available_slots_per_day[formatted_date]:
                    booked_slots = 0
                    booked_dlkt_slots = 0
                    for booked_slot in grouped_appointments.get(formatted_date, []):
                        if booked_slot.get('start_time') \
                                <= actual_slot.get('start_time') \
                                < booked_slot.get('end_time') \
                                or \
                                actual_slot.get('end_time') \
                                > booked_slot.get('start_time') \
                                >= actual_slot.get('start_time'):
                            # print('>>>actual_slot.get(start_time)', actual_slot.get('start_time'))
                            # print('>>>actual_slot.get(end_time)', actual_slot.get('end_time'))
                            # print('>>>booked_slot.get(start_time)', booked_slot.get('start_time'))
                            # print('>>>booked_slot.get(end_time)', booked_slot.get('end_time'))
                            # print('>>>booked_slot.get(blackout_flag)', booked_slot.get('blackout_flag', False))


                            if booked_slot.get('blackout_flag', False):  # If it's blackout override the no of slots
                                actual_slot['no_of_slots'] = 0
                            else:
                                if  booked_slot['is_dlkt']:
                                    booked_dlkt_slots += 1
                                else:   
                                    booked_slots += 1   
                    if service_is_dltk:
                        dlkt_nos = actual_slot['no_of_dlkt_slots'] - booked_dlkt_slots
                        if actual_slot['no_of_slots'] <= (booked_slots + booked_dlkt_slots):
                            actual_slot['no_of_slots'] = 0
                        elif actual_slot['no_of_slots'] - booked_slots >= dlkt_nos:
                            actual_slot['no_of_slots'] = dlkt_nos
                        else: 
                            actual_slot['no_of_slots'] = dlkt_nos - (actual_slot['no_of_slots'] - booked_slots) 
                    else:
                       actual_slot['no_of_slots']  =  actual_slot['no_of_slots'] - (booked_slots + booked_dlkt_slots)

                    del actual_slot['no_of_dlkt_slots'] # no need to expose
                       
                    if format_time:  # If true send formatted time
                        actual_slot['start_time'] = actual_slot['start_time'].strftime('%H:%M')
                        actual_slot['end_time'] = actual_slot['end_time'].strftime('%H:%M')

            return AvailabilityService.prune_appointments(available_slots_per_day)

        except exc.SQLAlchemyError as e:
            print(e)
            return {'message': 'API is down'}, 500

    @staticmethod
    def has_available_slots(office: Office, start_time:datetime, end_time: datetime, service: Service):
        """Return if there is any available slot for the time period for the office."""
        start_time = start_time.astimezone(pytz.timezone(office.timezone.timezone_name))
        end_time = end_time.astimezone(pytz.timezone(office.timezone.timezone_name))

        available_day_slots = AvailabilityService.get_available_slots(office=office, days=[start_time], format_time=False, service=service)

        has_available_slot = False
        for slot in available_day_slots[start_time.strftime('%m/%d/%Y')]:  # Iterate the only item from the list
            # Because services can be artbitary duration, we just check if times fall within duration
            # e.g slot is 8-9, but start_time/end_time are 8:30-8:45.
            # We do NOT check across slots, only within an individual slot
            if slot['start_time'] <= start_time.time() and slot['end_time'] >= end_time.time():
                has_available_slot = True

        return has_available_slot

    @staticmethod
    def group_appointments(appointments, timezone: str):
        filtered_appointments = {}
        for app in appointments:
            formatted_date = app.start_time.astimezone(pytz.timezone(timezone)).strftime('%m/%d/%Y')
            if not filtered_appointments.get(formatted_date, None):
                filtered_appointments[formatted_date] = []
            filtered_appointments[formatted_date].append({
                'start_time': app.start_time.astimezone(pytz.timezone(timezone)).time(),
                'end_time': app.end_time.astimezone(pytz.timezone(timezone)).time(),
                'blackout_flag': app.blackout_flag == 'Y' or app.stat_flag,
                'is_dlkt': (app.service.is_dlkt == YesNo.YES) if app.service else False
            })
        return filtered_appointments

    @staticmethod
    def prune_appointments(available_slots_per_day: Dict):
        for key, slots in available_slots_per_day.items():
            for slot in reversed(slots):
                if slot['no_of_slots'] <= 0:
                    slots.remove(slot)

        return available_slots_per_day
