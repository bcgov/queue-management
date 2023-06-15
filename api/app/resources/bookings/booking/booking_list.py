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

import logging
from flask import request
from flask_restx import Resource
from sqlalchemy import exc
from app.models.bookings import Booking
from app.models.theq import CSR
from app.schemas.bookings import BookingSchema
from qsystem import api
from app.utilities.auth_util import Role, get_username
from app.auth.auth import jwt


@api.route("/bookings/", methods=["GET"])
class BookingList(Resource):

    booking_schema = BookingSchema(many=True)

    @jwt.has_one_of_roles([Role.internal_user.value])
    def get(self):

        csr = CSR.find_by_username(get_username())
        office_filter = csr.office_id

        if request.args.get('office_id') and csr.ita2_designate == 1:
            office_filter = request.args.get('office_id')

        try:
            bookings = Booking.query.filter_by(office_id=office_filter).all()
            result = self.booking_schema.dump(bookings)
            return {'bookings': result,
                    'errors': self.booking_schema.validate(bookings)}, 200

        except exc.SQLAlchemyError as error:
            logging.error(error, exc_info=True)
            return {"message": "API is down"}, 500
