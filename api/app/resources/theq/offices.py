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
import logging

from flask import request
from flask_restx import Resource
from qsystem import api, db
from sqlalchemy import exc
from app.models.theq import Office, Service
from app.schemas.theq import OfficeSchema
from app.services import AvailabilityService
from app.utilities.timezone_utils import get_timezone


@api.route("/offices", methods=["GET"])
class OfficesByService(Resource):

    @staticmethod
    def _get_next_appointment_date(office, service):
        timezone = get_timezone(office.timezone.timezone_name)
        today = datetime.datetime.now().astimezone(timezone)
        days = [
            today + datetime.timedelta(days=day)
            for day in range(office.appointments_days_limit or 0)
        ]

        if not days:
            return None

        available_slots = AvailabilityService.get_available_slots(
            office=office, days=days, service=service
        )
        for day in days:
            if available_slots.get(day.strftime('%m/%d/%Y')):
                return day.date().isoformat()

        return None

    def get(self):
        try:
            service_id = int(request.args.get('service_id'))
        except (TypeError, ValueError):
            return {'message': 'service_id must be an integer.'}, 400

        try:
            service = db.session.get(Service, service_id)
            if service is None:
                return {'offices': [],
                        'errors': {}}

            offices = Office.query.join(Office.services).filter(
                Service.service_id == service_id,
                Office.deleted.is_(None)
            ).order_by(Office.office_name).all()
            result = OfficeSchema(many=True).dump(offices)

            for office, serialized_office in zip(offices, result):
                serialized_office['next_appointment_date'] = self._get_next_appointment_date(
                    office, service
                )

            return {'offices': result,
                    'errors': {}}

        except exc.SQLAlchemyError as exception:
            logging.exception(exception)
            return {'message': 'API is down'}, 500


@api.route("/offices/", methods=["GET"])
class OfficeList(Resource):

    def get(self):
        try:

            result = Office.get_all_active_offices()

            return {'offices': result,
                    'errors': {}}

        except exc.SQLAlchemyError as exception:
            logging.exception(exception)
            return {'message': 'API is down'}, 500
