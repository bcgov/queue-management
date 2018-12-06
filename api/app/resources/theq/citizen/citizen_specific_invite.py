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
from flask_restplus import Resource
from qsystem import api, api_call_with_retry, db, oidc, socketio
from app.models.theq import Citizen, CSR
from app.models.theq import SRState
from app.schemas.theq import CitizenSchema


@api.route("/citizens/<int:id>/invite/", methods=["POST"])
class CitizenSpecificInvite(Resource):

    citizen_schema = CitizenSchema()

    @oidc.accept_token(require_token=True)
    @api_call_with_retry
    def post(self, id):
        lock = FileLock("lock/invite_citizen.lock")

        with lock:
            csr = CSR.find_by_username(g.oidc_token_info['username'])
            citizen = db.session.query(Citizen).with_lockmode('update').filter_by(citizen_id=id).first()
            active_service_state = SRState.get_state_by_name("Active")

            active_service_request = citizen.get_active_service_request()

            if active_service_request is None:
                return {"message": "Citizen has no active service requests"}, 400

            try:
                active_service_request.invite(csr)
            except TypeError:
                return {"message": "Citizen  has already been invited"}, 400

            active_service_request.sr_state_id = active_service_state.sr_state_id

            db.session.add(citizen)
            db.session.commit()

            socketio.emit('update_customer_list', {}, room=csr.office_id)
            socketio.emit('citizen_invited', {}, room='sb-%s' % csr.office.office_number)
            result = self.citizen_schema.dump(citizen)
            socketio.emit('update_active_citizen', result.data, room=csr.office_id)

        return {'citizen': result.data,
                'errors': result.errors}, 200
