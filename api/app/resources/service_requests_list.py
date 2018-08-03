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

from flask import request, g
from flask_restplus import Resource
from datetime import datetime
from qsystem import api, api_call_with_retry, db, oidc
from app.models import Citizen, CitizenState, Channel, CSR, Period, PeriodState, Service, ServiceReq, SRState
from app.schemas import ChannelSchema, ServiceReqSchema
from marshmallow import ValidationError


@api.route("/service_requests/", methods=["POST"])
class ServiceRequestsList(Resource):

    channel_schema = ChannelSchema()
    service_request_schema = ServiceReqSchema()

    @oidc.accept_token(require_token=True)
    @api_call_with_retry
    def post(self):
        json_data = request.get_json()

        if not json_data:
            return {"message": "No input data received for creating service request"}, 400

        csr = CSR.query.filter_by(username=g.oidc_token_info['username']).first()

        try:
            service_request = self.service_request_schema.load(json_data['service_request']).data

        except ValidationError as err:
            return {"message": err.messages}, 422
        except KeyError as err:
            print (err)
            return {"message": str(err)}

        active_sr_state = SRState.query.filter_by(sr_code='Active').first()
        citizen_state = CitizenState.query.filter_by(cs_state_name="Active").first()
        citizen = Citizen.query.get(service_request.citizen_id)
        service = Service.query.get(service_request.service_id)

        if citizen is None:
            return {"message": "No matching citizen found for citizen_id"}, 400

        if service is None:
            return {"message": "No matching citizen found for citizen_id"}, 400

        service_request.sr_state = active_sr_state

        # Only add ticket creation period and ticket number if it's their first service_request
        if len(citizen.service_reqs) <= 1:
            period_state_ticket_creation = PeriodState.query.filter_by(ps_name="Ticket Creation").first()

            ticket_create_period = Period(
                csr_id=csr.csr_id,
                reception_csr_ind=csr.receptionist_ind,
                ps_id=period_state_ticket_creation.ps_id,
                time_start=citizen.get_service_start_time(),
                time_end=datetime.now(),
                accurate_time_ind=1
            )
            service_request.periods.append(ticket_create_period)

            service_count = ServiceReq.query \
                    .join(ServiceReq.citizen, aliased=True) \
                    .filter(Citizen.start_time >= citizen.start_time.strftime("%Y-%m-%d")) \
                    .filter_by(office_id=csr.office_id) \
                    .join(ServiceReq.service, aliased=True) \
                    .filter_by(prefix=service.prefix) \
                    .count()

            citizen.ticket_number = service.prefix + str(service_count)
        else:
            period_state_being_served = PeriodState.query.filter_by(ps_name="Being Served").first()

            ticket_create_period = Period(
                csr_id=csr.csr_id,
                reception_csr_ind=csr.receptionist_ind,
                ps_id=period_state_being_served.ps_id,
                time_start=datetime.now(),
                accurate_time_ind=1
            )
            service_request.periods.append(ticket_create_period)

        citizen.cs_id = citizen_state.cs_id

        db.session.add(service_request)
        db.session.add(citizen)
        db.session.commit()

        result = self.service_request_schema.dump(service_request)

        return {'service_request': result.data,
                'errors': result.errors}, 201
