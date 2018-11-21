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

from datetime import datetime
from flask import request, g
from flask_restplus import Resource
from marshmallow import ValidationError

from qsystem import api, api_call_with_retry, db, oidc, socketio
from app.models import CSR, Period, PeriodState, ServiceReq, SRState
from app.schemas import CitizenSchema, ServiceReqSchema
from ..models.citizen import Citizen
from ..utilities.snowplow import SnowPlow


@api.route("/service_requests/<int:id>/", methods=["PUT"])
class ServiceRequestsDetail(Resource):

    citizen_schema = CitizenSchema()
    service_requests_schema = ServiceReqSchema(many=True)
    service_request_schema = ServiceReqSchema()

    @oidc.accept_token(require_token=True)
    @api_call_with_retry
    def put(self, id):
        json_data = request.get_json()

        if not json_data:
            return {'message': 'No input data received for updating citizen'}, 400

        csr = CSR.find_by_username(g.oidc_token_info['username'])

        service_request = ServiceReq.query.filter_by(sr_id=id) \
                .join(ServiceReq.citizen, aliased=True) \
                .filter_by(office_id=csr.office_id).first_or_404()
        try:
            service_request = self.service_request_schema.load(json_data, instance=service_request, partial=True).data

        except ValidationError as err:
            return {'message': err.messages}, 422

        db.session.add(service_request)
        db.session.commit()

        SnowPlow.choose_service(service_request, csr, "chooseservice")

        result = self.service_request_schema.dump(service_request)
        citizen_result = self.citizen_schema.dump(service_request.citizen)
        socketio.emit('update_active_citizen', citizen_result.data, room=csr.office_id)

        return {'service_request': result.data,
                'errors': result.errors}, 200


@api.route("/service_requests/<int:id>/activate/", methods=["POST"])
class ServiceRequestActivate(Resource):

    citizen_schema = CitizenSchema()
    service_requests_schema = ServiceReqSchema(many=True)
    service_request_schema = ServiceReqSchema()

    @oidc.accept_token(require_token=True)
    @api_call_with_retry
    def post(self, id):

        csr = CSR.find_by_username(g.oidc_token_info['username'])

        service_request = ServiceReq.query.filter_by(sr_id=id) \
            .join(ServiceReq.citizen, aliased=True) \
            .filter_by(office_id=csr.office_id).first_or_404()

        active_service_state = SRState.get_state_by_name("Active")
        complete_service_state = SRState.get_state_by_name("Complete")

        # Find the currently active service_request and close it
        for req in service_request.citizen.service_reqs:
            if req.sr_state_id == active_service_state.sr_state_id:
                req.sr_state_id = complete_service_state.sr_state_id
                req.finish_service(csr, clear_comments=False)
                db.session.add(req)

        # Then set the requested service to active
        service_request.sr_state_id = active_service_state.sr_state_id

        period_state_being_served = PeriodState.get_state_by_name("Being Served")

        new_period = Period(
            sr_id=service_request.sr_id,
            csr_id=csr.csr_id,
            reception_csr_ind=csr.receptionist_ind,
            ps_id=period_state_being_served.ps_id,
            time_start=datetime.now()
        )

        db.session.add(new_period)
        db.session.add(service_request)

        citizen_obj = Citizen.query.get(service_request.citizen_id)
        citizen_obj.service_count = citizen_obj.service_count + 1

        db.session.commit()

        SnowPlow.choose_service(service_request, csr, "additionalservice")

        citizen_result = self.citizen_schema.dump(service_request.citizen)
        socketio.emit('update_active_citizen', citizen_result.data, room=csr.office_id)
        result = self.service_request_schema.dump(service_request)

        return {'service_request': result.data,
                'errors': result.errors}, 200
