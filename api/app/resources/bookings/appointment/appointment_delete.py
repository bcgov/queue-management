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

from flask import abort, g
from flask_restx import Resource
from app.models.bookings import Appointment
from app.schemas.bookings import AppointmentSchema
from app.models.theq import CSR, PublicUser, Citizen, Office, Timezone
from qsystem import api, db, oidc
from app.utilities.snowplow import SnowPlow
from app.utilities.email import send_cancel_email
from app.utilities.auth_util import is_public_user


@api.route("/appointments/<int:id>/", methods=["DELETE"])
class AppointmentDelete(Resource):

    appointment_schema = AppointmentSchema()

    @oidc.accept_token(require_token=True)
    def delete(self, id):

        appointment = Appointment.query.filter_by(appointment_id=id)\
                                       .first_or_404()

        csr = None if is_public_user() else CSR.find_by_username(g.oidc_token_info['username'])

        user: PublicUser = PublicUser.find_by_username(g.oidc_token_info['username']) if is_public_user() else None
        if is_public_user():
            # Check if it's a public user
            citizen = Citizen.find_citizen_by_id(appointment.citizen_id)
            if not citizen or citizen.citizen_id != appointment.citizen_id:
                abort(403)

        # TODO handle public user case here
        if csr:
            SnowPlow.snowplow_appointment(None, csr, appointment, 'appointment_delete')

        db.session.delete(appointment)
        db.session.commit()

        # If the appointment is public user's and if staff deletes it send email
        if csr:
            office = Office.find_by_id(appointment.office_id)
            send_cancel_email(appointment, user, office, office.timezone)

        return {}, 204
