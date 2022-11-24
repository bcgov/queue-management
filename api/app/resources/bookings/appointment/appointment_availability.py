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

import datetime, logging

import pytz
from flask_restx import Resource
from flask import request
from sqlalchemy import exc

from app.models.theq import Office
from app.models.theq import Service
from app.services import AvailabilityService
from qsystem import api
from app.auth.auth import jwt


@api.route("/offices/<int:office_id>/slots/", methods=["GET"])
class OfficeSlots(Resource):

    def get(self, office_id: int):
        try:
            office = Office.find_by_id(office_id)

            appointments_days_limit = office.appointments_days_limit

            # Dictionary to store the available slots per day
            tz = pytz.timezone(office.timezone.timezone_name)

            # today's date and time
            today = datetime.datetime.now().astimezone(tz)

            # Get all the dates from today until booking is allowed
            days = [today + datetime.timedelta(days=x) for x in range(appointments_days_limit)]

            service = None
            service_id = request.args.get('service_id')
            if (service_id):
                service = Service.query.get(int(service_id))

            return AvailabilityService.get_available_slots(office=office, days=days, service=service)

        except exc.SQLAlchemyError as exception:
            logging.exception(exception)
            return {'message': 'API is down'}, 500
