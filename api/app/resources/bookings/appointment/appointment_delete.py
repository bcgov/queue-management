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

from pprint import pprint

from flask import request, abort, g
from flask_restx import Resource

from app.models.bookings import Appointment
from app.models.theq import CSR, PublicUser, Citizen, Office
from app.schemas.bookings import AppointmentSchema
from app.utilities.auth_util import Role, has_any_role
from app.utilities.auth_util import is_public_user
from app.utilities.email import get_cancel_email_contents, send_email
from app.utilities.snowplow import SnowPlow
from qsystem import application
from qsystem import api, db, socketio
from app.auth.auth import jwt


@api.route("/appointments/<int:id>/", methods=["DELETE"])
class AppointmentDelete(Resource):
    appointment_schema = AppointmentSchema()

    @jwt.has_one_of_roles([Role.internal_user.value, Role.online_appointment_user.value])
    def delete(self, id):

        appointment = Appointment.query.filter_by(appointment_id=id) \
            .first_or_404()

        csr = None if is_public_user() else CSR.find_by_username(g.jwt_oidc_token_info['username'])

        user: PublicUser = PublicUser.find_by_username(g.jwt_oidc_token_info['username']) if is_public_user() else None
        if is_public_user():
            # Check if it's a public user
            citizen = Citizen.find_citizen_by_id(appointment.citizen_id)
            if not citizen or citizen.citizen_id != appointment.citizen_id:
                abort(403)

        # Must call this prior to deleting from DB, so cannot 
        # combine with repeated is_draft check below
        if not appointment.is_draft:
            SnowPlow.snowplow_appointment(None, csr, appointment, 'appointment_delete')

        # Do not log snowplow events or send emails if it's a draft.
        # If the appointment is public user's and if staff deletes it send email
        if not appointment.is_draft and csr:

            office = Office.find_by_id(appointment.office_id)

            # Send blackout email
            try:
                send_email(request.headers['Authorization'].replace('Bearer ', ''), *get_cancel_email_contents(appointment, user, office, office.timezone))
            except Exception as exc:
                pprint(f'Error on token generation - {exc}')

        db.session.delete(appointment)
        db.session.commit()

        if not application.config['DISABLE_AUTO_REFRESH']:
            socketio.emit('appointment_delete', id)

        return {}, 204
