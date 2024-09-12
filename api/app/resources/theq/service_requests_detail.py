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

from datetime import datetime, timezone
from flask import request
from flask_restx import Resource
from marshmallow import ValidationError
from qsystem import api, api_call_with_retry, db, socketio
from app.models.theq import CSR, Period, PeriodState, ServiceReq, SRState
from app.schemas.theq import CitizenSchema, ServiceReqSchema
from app.models.theq.citizen import Citizen
from app.utilities.snowplow import SnowPlow
from app.utilities.auth_util import Role, get_username
from app.auth.auth import jwt


@api.route("/service_requests/<int:id>/", methods=["PUT"])
class ServiceRequestsDetail(Resource):

    citizen_schema = CitizenSchema()
    service_requests_schema = ServiceReqSchema(many=True)
    service_request_schema = ServiceReqSchema()

    @jwt.has_one_of_roles([Role.internal_user.value])
    @api_call_with_retry
    def put(self, id):
        json_data = request.get_json()

        if not json_data:
            return {'message': 'No input data received for updating citizen'}, 400

        csr = CSR.find_by_username(get_username())

        service_request = ServiceReq.query.filter_by(sr_id=id) \
                .join(ServiceReq.citizen, aliased=True).first_or_404()

        try:
            service_request = self.service_request_schema.load(json_data, instance=service_request, partial=True)

        except ValidationError as err:
            return {'message': err.messages}, 422

        db.session.add(service_request)
        db.session.commit()

        SnowPlow.choose_service(service_request, csr, "chooseservice")

        result = self.service_request_schema.dump(service_request)
        citizen_result = self.citizen_schema.dump(service_request.citizen)
        socketio.emit('update_active_citizen', citizen_result, room=csr.office.office_name)

        return {'service_request': result,
                'errors': self.service_request_schema.validate(service_request)}, 200


@api.route("/service_requests/<int:id>/activate/", methods=["POST"])
class ServiceRequestActivate(Resource):

    citizen_schema = CitizenSchema()
    service_requests_schema = ServiceReqSchema(many=True)
    service_request_schema = ServiceReqSchema()

    @jwt.has_one_of_roles([Role.internal_user.value])
    @api_call_with_retry
    def post(self, id):
        csr = CSR.find_by_username(get_username())

        service_request = ServiceReq.query.filter_by(sr_id=id) \
            .join(ServiceReq.citizen, aliased=True) \
            .filter_by(office_id=csr.office_id).first_or_404()

        active_service_state = SRState.get_state_by_name("Active")
        complete_service_state = SRState.get_state_by_name("Complete")

        # Find the currently active service_request and close it
        current_sr_number = 0
        for req in service_request.citizen.service_reqs:
            if req.sr_state_id == active_service_state.sr_state_id:
                req.sr_state_id = complete_service_state.sr_state_id
                req.finish_service(csr, clear_comments=False)
                current_sr_number = req.sr_number
                db.session.add(req)

        # Then set the requested service to active
        service_request.sr_state_id = active_service_state.sr_state_id

        period_state_being_served = PeriodState.get_state_by_name("Being Served")

        new_period = Period(
            sr_id=service_request.sr_id,
            csr_id=csr.csr_id,
            reception_csr_ind=csr.receptionist_ind,
            ps_id=period_state_being_served.ps_id,
            time_start=datetime.now(timezone.utc)
        )

        db.session.add(new_period)
        db.session.add(service_request)

        db.session.commit()

        #  To make service active, stop current service, restart previous service.
        SnowPlow.snowplow_event(service_request.citizen.citizen_id, csr, "stopservice", current_sr_number=current_sr_number)
        SnowPlow.snowplow_event(service_request.citizen.citizen_id, csr, "restartservice", current_sr_number=service_request.sr_number)

        citizen_result = self.citizen_schema.dump(service_request.citizen)
        socketio.emit('update_active_citizen', citizen_result, room=csr.office.office_name)
        result = self.service_request_schema.dump(service_request)

        return {'service_request': result,
                'errors': self.service_request_schema.validate(service_request)}, 200
