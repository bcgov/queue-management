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
from flask import g
from flask_restx import Resource
from qsystem import api, api_call_with_retry, db, socketio, my_print, application
from app.models.theq import Citizen, CSR
from app.models.theq import SRState
from app.models.bookings import Appointment
from app.schemas.bookings import AppointmentSchema
from app.schemas.theq import CitizenSchema
from app.utilities.snowplow import SnowPlow
from app.utilities.auth_util import Role, has_any_role
from app.auth.auth import jwt

# To remove from queue and restore to calendar
# - Setting `checked_in_time` to null > restores it in calendar
# - 


@api.route("/citizens/<int:id>/remove_from_queue/", methods=["POST"])
class CitizenRemoveFromQueue(Resource):

    citizen_schema = CitizenSchema()
    appointment_schema = AppointmentSchema()

    @jwt.has_one_of_roles([Role.internal_user.value])
    @api_call_with_retry
    def post(self, id):
        csr = CSR.find_by_username(g.jwt_oidc_token_info['username'])
        citizen = Citizen.query.filter_by(citizen_id=id).first()
        active_service_request = citizen.get_active_service_request()

        my_print("==> POST /citizens/" + str(citizen.citizen_id) + '/remove_from_queue, Ticket: ' + citizen.ticket_number)

        if active_service_request is None:
            return {"message": "Citizen has no active service requests"}

        appointment = Appointment.query.filter_by(citizen_id=id) \
            .filter_by(office_id=csr.office_id) \
            .filter(Appointment.checked_in_time.isnot(None)) \
            .first_or_404()

        # This "un-check-in"s the appointment, returning it to calendar and removing from the queue.
        appointment.checked_in_time = None

        # Delete all "periods", FKs on service req
        active_service_request.remove_from_queue()
        # Delete the service req. 
        db.session.delete(active_service_request)
        db.session.commit()

        # appointment, warning = self.appointment_schema.load(json_data, instance=appointment, partial=True)
        # if warning:
        #     logging.warning("WARNING: %s", warning)
        #     return {"message": warning}, 422

        socketio.emit('update_customer_list', {}, room=csr.office.office_name)
        socketio.emit('citizen_invited', {}, room='sb-%s' % csr.office.office_number)
        result = self.appointment_schema.dump(appointment)

        if not application.config['DISABLE_AUTO_REFRESH']:
            socketio.emit('appointment_create', result)

        return {"appointment": result,
                "errors": self.appointment_schema.validate(appointment)}, 200

