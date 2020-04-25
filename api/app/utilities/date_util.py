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
from datetime import datetime as dt, timedelta, time
import calendar
import datetime as dt


# def get_first_and_last_dates_of_month(month: int, year: int):
#     """Return first and last dates for a given month and year."""
#     start_date = dt.now().replace(day=1, year=year, month=month)
#     start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
#
#     end_date = start_date.replace(day=calendar.monthrange(year=year, month=month)[1])
#     end_date = end_date.replace(hour=23, minute=59, second=59, microsecond=999999)
#
#     return start_date, end_date


def add_delta_to_time(time: time, minutes: int=0, seconds:int=0):
    """Add delta in minutes to the time"""
    time_combine = dt.datetime.combine(dt.date(1, 1, 1), time)
    if minutes > 0 :
        delta_time = time_combine + timedelta(minutes=minutes)
    else:
        delta_time = time_combine - timedelta(minutes=minutes)
    if seconds > 0:
        delta_time += timedelta(seconds=seconds)
    else:
        delta_time -= timedelta(seconds=seconds)

    return delta_time.time()
