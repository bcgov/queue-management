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
from datetime import datetime, timedelta
from qsystem import api, api_call_with_retry, db, oidc, socketio
from app.models import Citizen, CitizenState, CSR, Period, PeriodState, Service, ServiceReq, SRState
from app.schemas import CitizenSchema, ServiceReqSchema
from marshmallow import ValidationError
from ..utilities.snowplow import SnowPlow

@api.route("/service_requests/", methods=["POST"])
class ServiceRequestsList(Resource):

    citizen_schema = CitizenSchema()
    service_request_schema = ServiceReqSchema()

    @oidc.accept_token(require_token=True)
    @api_call_with_retry
    def post(self):
        json_data = request.get_json()

        if not json_data:
            return {"message": "No input data received for creating service request"}, 400

        csr = CSR.find_by_username(g.oidc_token_info['username'])

        try:
            service_request = self.service_request_schema.load(json_data['service_request']).data

        except ValidationError as err:
            return {"message": err.messages}, 422
        except KeyError as err:
            print (err)
            return {"message": str(err)}

        active_sr_state = SRState.get_state_by_name("Active")
        complete_sr_state = SRState.get_state_by_name("Complete")
        citizen_state = CitizenState.query.filter_by(cs_state_name="Active").first()
        citizen = Citizen.query.get(service_request.citizen_id)
        service = Service.query.get(service_request.service_id)

        if citizen is None:
            return {"message": "No matching citizen found for citizen_id"}, 400

        if service is None:
            return {"message": "No matching service found for service_id"}, 400

        # Find the currently active service_request and close it (if it exists)
        for req in citizen.service_reqs:
            if req.sr_state_id == active_sr_state.sr_state_id:
                req.sr_state_id = complete_sr_state.sr_state_id
                req.finish_service(csr, clear_comments=False)
                db.session.add(req)

        service_request.sr_state_id = active_sr_state.sr_state_id

        # Only add ticket creation period and ticket number if it's their first service_request
        if len(citizen.service_reqs) == 0:
            period_state_ticket_creation = PeriodState.get_state_by_name("Ticket Creation")

            ticket_create_period = Period(
                csr_id=csr.csr_id,
                reception_csr_ind=csr.receptionist_ind,
                ps_id=period_state_ticket_creation.ps_id,
                time_start=citizen.get_service_start_time(),
                time_end=datetime.now()
            )
            service_request.periods.append(ticket_create_period)

            # Move start_time back 6 hours to account for DST and UTC offsets
            # It's only important that the number carries over _around_ midnight
            offset_start_time = citizen.start_time - timedelta(hours=6)

            service_count = ServiceReq.query \
                    .join(ServiceReq.citizen, aliased=True) \
                    .filter(Citizen.start_time >= offset_start_time.strftime("%Y-%m-%d")) \
                    .filter_by(office_id=csr.office_id) \
                    .join(ServiceReq.service, aliased=True) \
                    .filter_by(prefix=service.prefix) \
                    .count()

            citizen.ticket_number = service.prefix + str(service_count)
        else:
            period_state_being_served = PeriodState.get_state_by_name("Being Served")

            ticket_create_period = Period(
                csr_id=csr.csr_id,
                reception_csr_ind=csr.receptionist_ind,
                ps_id=period_state_being_served.ps_id,
                time_start=datetime.now()
            )
            service_request.periods.append(ticket_create_period)

        citizen.cs_id = citizen_state.cs_id

        #  See whether first service, or next service.
        if len(citizen.service_reqs) == 0:
            snowplow_event = "chooseservice"
            citizen.service_count = 1
        else:
            snowplow_event = "additionalservice"
            citizen.service_count = citizen.service_count + 1

        db.session.add(service_request)
        db.session.add(citizen)
        db.session.commit()

        SnowPlow.choose_service(service_request, csr, snowplow_event)

        citizen_result = self.citizen_schema.dump(citizen)
        socketio.emit('update_active_citizen', citizen_result.data, room=csr.office_id)
        result = self.service_request_schema.dump(service_request)

        return {'service_request': result.data,
                'errors': result.errors}, 201
