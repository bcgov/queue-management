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
import datetime as dt
from datetime import timedelta, time

days_mapping = {
    'Monday': 1,
    'Tuesday': 2,
    'Wednesday': 3,
    'Thursday': 4,
    'Friday': 5,
    'Saturday': 6,
    'Sunday': 7
}


def add_delta_to_time(time: time, minutes: int = 0, seconds: int = 0):
    """Add delta in minutes to the time"""
    time_combine = dt.datetime.combine(dt.date(1, 1, 1), time)
    if minutes > 0:
        delta_time = time_combine + timedelta(minutes=minutes)
    else:
        delta_time = time_combine - timedelta(minutes=minutes)
    if seconds > 0:
        delta_time += timedelta(seconds=seconds)
    else:
        delta_time -= timedelta(seconds=seconds)

    return delta_time.time()


def day_indexes(days):
    """Return the integer index with respect to the string."""
    integer_indexes = list()
    for day in days:
        integer_indexes.append(days_mapping[day])
    return integer_indexes
