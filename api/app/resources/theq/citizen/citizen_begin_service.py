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

from filelock import FileLock
from flask import g
from flask_restx import Resource
from qsystem import api, api_call_with_retry, db, socketio, my_print
from app.models.theq import Citizen, CSR
from app.models.theq import SRState
from app.schemas.theq import CitizenSchema
from app.utilities.auth_util import Role, has_any_role
from app.auth.auth import jwt


@api.route("/citizens/<int:id>/begin_service/", methods=["POST"])
class CitizenBeginService(Resource):

    citizen_schema = CitizenSchema()

    @jwt.has_one_of_roles([Role.internal_user.value])
    @api_call_with_retry
    def post(self, id):
        csr = CSR.find_by_username(g.jwt_oidc_token_info['username'])
        lock = FileLock("lock/begin_citizen_{}.lock".format(csr.office_id))

        with lock:
            citizen = Citizen.query.filter_by(citizen_id=id).first()
            pending_service_state = SRState.get_state_by_name("Active")

            if citizen is None:
                print("==> POST /citizen/<id>/begin_service/ error. No citizen with id " + str(id))
                return {"message": "No citizen found with id " + str(id)}
            else:
                my_print("==> POST /citizens/" + str(citizen.citizen_id) + '/begin_service/, Ticket: '
                         + citizen.ticket_number)

            active_service_request = citizen.get_active_service_request()

            if active_service_request is None:
                return {"message": "Citizen has no active service requests"}

            try:
                #  Get Snowplow call.
                active_period = active_service_request.get_active_period()
                snowplow_event = "beginservice"
                if active_period.ps.ps_name == "On hold":
                    snowplow_event = "invitefromhold"
                if active_period.ps.ps_name == "Ticket Creation":
                    snowplow_event = "servecitizen"

                active_service_request.begin_service(csr, snowplow_event)
            except TypeError:
                return {"message": "Citizen  has already been invited"}, 400

            active_service_request.sr_state_id = pending_service_state.sr_state_id

            db.session.add(citizen)
            db.session.commit()

            if snowplow_event != "beginservice":
                socketio.emit('update_customer_list', {}, room=csr.office.office_name)
                
            result = self.citizen_schema.dump(citizen)
            socketio.emit('update_active_citizen', result, room=csr.office.office_name)

        return {'citizen': result,
                'errors': self.citizen_schema.validate(citizen)}, 200
