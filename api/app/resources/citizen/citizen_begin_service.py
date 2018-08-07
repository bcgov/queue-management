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

from flask import g
from flask_restplus import Resource
from qsystem import api, api_call_with_retry, db, oidc, socketio
from app.models import Citizen, CSR
from app.models import SRState
from app.schemas import CitizenSchema


@api.route("/citizens/<int:id>/begin_service/", methods=["POST"])
class CitizenBeginService(Resource):

    citizen_schema = CitizenSchema()

    @oidc.accept_token(require_token=True)
    @api_call_with_retry
    def post(self, id):
        csr = CSR.query.filter_by(username=g.oidc_token_info['username']).first()
        citizen = Citizen.query.filter_by(citizen_id=id, office_id=csr.office_id).first()
        active_service_request = citizen.get_active_service_request()

        if active_service_request is None:
            return {"message": "Citizen has no active service requests"}

        active_service_request.begin_service(csr)
        pending_service_state = SRState.query.filter_by(sr_code='Active').first()
        active_service_request.sr_state_id = pending_service_state.sr_state_id

        db.session.add(citizen)
        db.session.commit()

        socketio.emit('update_customer_list', {}, room=csr.office_id)

        result = self.citizen_schema.dump(citizen)
        return {'citizen': result.data,
                'errors': result.errors}, 200
