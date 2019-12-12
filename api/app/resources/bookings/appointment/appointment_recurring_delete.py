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
from app.models.bookings import Appointment
from app.schemas.bookings import AppointmentSchema
from app.models.theq import CSR
from qsystem import api, db, oidc


@api.route("/appointments/recurring/<string:id>", methods=["DELETE"])
class AppointmentRecurringDelete(Resource):

    appointment_schema = AppointmentSchema()

    @oidc.accept_token(require_token=True)
    def delete(self, id):

        csr = CSR.find_by_username(g.oidc_token_info['username'])

        appointments = Appointment.query.filter_by(recurring_uuid=id)\
                                        .filter_by(office_id=csr.office_id)\
                                        .all()

        for appointment in appointments:
            db.session.delete(appointment)
            db.session.commit()

        return {}, 204
