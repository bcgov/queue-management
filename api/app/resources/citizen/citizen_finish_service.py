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
from qsystem import api, api_call_with_retry, db, oidc
from app.models import Citizen, CSR, CitizenState
from app.models import SRState
from app.schemas import CitizenSchema


@api.route("/citizens/<int:id>/finish_service/", methods=["POST"])
class CitizenFinishService(Resource):

    citizen_schema = CitizenSchema()

    @oidc.accept_token(require_token=True)
    @api_call_with_retry
    def post(self, id):
        csr = CSR.query.filter_by(username=g.oidc_token_info['username']).first()
        citizen = Citizen.query.filter_by(citizen_id=id, office_id=csr.office_id).first_or_404()
        active_service_request = citizen.get_active_service_request()

        if active_service_request is None:
            return {"message": "Citizen has no active service requests"}

        active_service_request.finish_service(csr)
        citizen_state = CitizenState.query.filter_by(cs_state_name="Received Services").first()
        citizen.cs_id = citizen_state.cs_id

        pending_service_state = SRState.query.filter_by(sr_code='Complete').first()
        active_service_request.sr_state_id = pending_service_state.sr_state_id

        db.session.add(active_service_request)
        db.session.commit()

        result = self.citizen_schema.dump(citizen)
        return {'citizen': result.data,
                'errors': result.errors}, 200
