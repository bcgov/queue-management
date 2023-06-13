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
from qsystem import api, db
from app.models.bookings import Booking, Room, Invigilator
from app.models.theq import CSR
from app.schemas.bookings import BookingSchema
from app.utilities.auth_util import Role, get_username
from app.auth.auth import jwt


@api.route("/bookings/recurring/<string:id>", methods=["PUT"])
class BookingRecurringPut(Resource):

    booking_schema = BookingSchema()

    @jwt.has_one_of_roles([Role.internal_user.value])
    def put(self, id):

        csr = CSR.find_by_username(get_username())

        json_data = request.get_json()

        if not json_data:
            return {"message": "No input data received for updating recurring bookings"}

        bookings = Booking.query.filter_by(recurring_uuid=id)\
                                .filter_by(office_id=csr.office_id)\
                                .all()

        for booking in bookings:

            booking = self.booking_schema.load(json_data, instance=booking, partial=True)
            warning = self.booking_schema.validate(json_data)

            if warning:
                logging.warning('WARNING: %s', warning)
                return {"message": warning}, 422

            db.session.add(booking)
            db.session.commit()

        result = self.booking_schema.dump(bookings)

        return {
            "bookings": result,
            "errors": self.booking_schema.validate(bookings)
        }, 200
