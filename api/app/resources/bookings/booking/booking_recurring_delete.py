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
from flask_restplus import Resource
from app.models.bookings import Booking
from app.schemas.bookings import BookingSchema
from app.models.theq import CSR
from qsystem import api, db, oidc


@api.route("/bookings/recurring/<string:id>", methods=["DELETE"])
class BookingRecurringDelete(Resource):

    booking_schema = BookingSchema

    @oidc.accept_token(require_token=True)
    def delete(self, id):

        print("==> In the python DELETE /bookings/recurring/<id> endpoint")

        csr = CSR.find_by_username(g.oidc_token_info['username'])

        bookings = Booking.query.filter_by(recurring_uuid=id).all()

        for booking in bookings:
            if booking.office_id != csr.office_id and csr.liaison_designate != 1:
                abort(404)

            db.session.delete(booking)
            db.session.commit()

        return {},204