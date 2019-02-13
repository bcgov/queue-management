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
from sqlalchemy import exc
from flask import abort, g, request
from flask_restplus import Resource
from app.models.bookings import Booking
from app.models.theq import CSR
from app.schemas.bookings import BookingSchema
from qsystem import api, oidc


@api.route("/bookings/<int:id>/", methods=["GET"])
class BookingDetail(Resource):

    booking_schema = BookingSchema()

    @oidc.accept_token(require_token=True)
    def get(self, id):

        csr = CSR.find_by_username(g.oidc_token_info['username'])

        try:
            booking = Booking.query.filter_by(booking_id=id).first_or_404()

            # Also 404 the request if they shouldn't be able to see this booking
            if booking.office_id != csr.office_id and csr.role.role_code != "LIAISON":
                abort(404)

            result = self.booking_schema.dump(booking)
            return {"booking": result.data,
                    "errors": result.errors}, 200

        except exc.SQLAlchemyError as error:
            logging.error(error, exc_info=True)
            return {"message": "API is down"}, 500
