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

from flask import abort, g, request
from flask_restx import Resource
from app.models.bookings import Booking
from app.schemas.bookings import BookingSchema
from app.models.theq import CSR
from qsystem import api, db
from datetime import datetime, timedelta, date
import logging, pytz
from app.utilities.auth_util import Role, has_any_role
from app.auth.auth import jwt


@api.route("/bookings/recurring/current-office/<string:id>", methods=["DELETE"])
class BookingRecurringDelete(Resource):

    booking_schema = BookingSchema
    timezone = pytz.timezone("US/Pacific")

    @jwt.has_one_of_roles([Role.internal_user.value])
    def delete(self, id):

        today = datetime.today()

        logging.info("==> In the python DELETE /bookings/recurring/<id> endpoint")

        csr = CSR.find_by_username(g.jwt_oidc_token_info['username'])

        bookings = Booking.query.filter_by(recurring_uuid=id)\
                                .filter_by(office_id=csr.office_id)\
                                .all()

        for booking in bookings:
            if booking.start_time.year == today.year and booking.start_time.month == today.month \
                    and booking.start_time.day == today.day and booking.start_time.hour <= 5:
                continue

            db.session.delete(booking)
            db.session.commit()

        return {},204



@api.route("/bookings/recurring/stat/<string:id>", methods=["DELETE"])
class BookingRecurringDelete(Resource):

    booking_schema = BookingSchema
    timezone = pytz.timezone("US/Pacific")

    @jwt.has_one_of_roles([Role.internal_user.value])
    def delete(self, id):

        today = datetime.today()

        logging.info("==> In the python DELETE /bookings/recurring/<id> endpoint")

        bookings = Booking.query.filter_by(recurring_uuid=id)\
                                .all()

        for booking in bookings:
            if booking.start_time.year == today.year and booking.start_time.month == today.month \
                    and booking.start_time.day == today.day and booking.start_time.hour <= 5:
                continue

            db.session.delete(booking)
            db.session.commit()

        return {},204