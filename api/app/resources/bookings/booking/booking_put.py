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
from flask import request, g
from flask_restplus import Resource
from qsystem import api, db, oidc
from app.models.bookings import Booking, Room
from app.models.theq import CSR
from app.schemas.bookings import BookingSchema


@api.route("/bookings/<int:id>/", methods=["PUT"])
class BookingPut(Resource):

    booking_schema = BookingSchema()

    @oidc.accept_token(require_token=True)
    def put(self, id):

        csr = CSR.find_by_username(g.oidc_token_info['username'])

        json_data = request.get_json()

        if not json_data:
            return {"message": "No input data received for updating a booking"}

        booking = Booking.query.filter_by(booking_id=id).first_or_404()

        booking, warning = self.booking_schema.load(json_data, instance=booking, partial=True)

        if warning:
            logging.warning("WARNING: %s", warning)
            return {"message": warning}, 422

        if booking.office_id == csr.office_id or csr.role.role_code == "LIAISON":

            db.session.add(booking)
            db.session.commit()

            result = self.booking_schema.dump(booking)

            return {"booking": result.data,
                    "errors": result.errors}, 200

        else:
            return {"The Booking Office ID and the CSR Office ID do not match!"}, 403
