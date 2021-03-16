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

from threading import Thread

from flask import abort, g, copy_current_request_context
from flask_restx import Resource

from app.models.bookings import Appointment
from app.models.theq import CSR, PublicUser, Citizen, Office
from app.schemas.bookings import AppointmentSchema
from app.utilities.auth_util import Role, has_any_role
from app.utilities.auth_util import is_public_user
from app.utilities.email import get_cancel_email_contents, send_email
from app.utilities.snowplow import SnowPlow
from qsystem import api, db, socketio, application


@api.route("/appointments/draft/<int:id>/", methods=["DELETE"])
class AppointmentDraftDelete(Resource):

    appointment_schema = AppointmentSchema()

    def delete(self, id):

        Appointment.delete_draft([id])
        if not application.config['DISABLE_AUTO_REFRESH']:
            socketio.emit('appointment_delete', id)

        return {}, 204

