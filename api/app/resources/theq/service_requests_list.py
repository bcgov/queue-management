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
from flask_restx import Resource
from datetime import datetime, timedelta
from qsystem import api, api_call_with_retry, db, socketio
from app.models.theq import Citizen, CitizenState, CSR, Period, PeriodState, Service, ServiceReq, SRState
from app.schemas.theq import CitizenSchema, ServiceReqSchema
from marshmallow import ValidationError
from app.utilities.snowplow import SnowPlow
import json
from app.utilities.auth_util import Role, has_any_role
from app.auth.auth import jwt

# Defining String constants to appease SonarQube
csr_const = "    --> CSR:       "
json_data_const = "    --> json_data: "

def get_service_request(self, json_data, csr):

    if not json_data:
        print("==> No json_data in POST /service_requests/")
        print(csr_const + csr.username)
        return (None, "No input data received for creating service request", 400)

    try:
        service_request = self.service_request_schema.load(json_data['service_request'])

    except ValidationError as err:
        print("==> ValidationError in POST /service_requests/")
        print(csr_const + csr.username)
        print(err)
        return (None, err.messages, 422)
    except KeyError as err:
        print("==> No service_request parameter in POST /service_requests/")
        print(csr_const + csr.username)
        print(json_data_const + json.dumps(json_data))
        print(err)
        return (None, str(err), 422)

    #  If service request is null, an error.
    if service_request is None:
        print("==> service_request is None in POST /service_requests/, error in schema.load")
        print(csr_const + csr.username)
        print(json_data_const + json.dumps(json_data['service_request']))
        return (None, "Service request is none trying to create service request", 400)

    #  All OK.  Return the service request.
    return (service_request, "", 200)

def get_service(service_request, json_data, csr):

    service = None
    try:
        service = Service.query.get(service_request.service_id)
    except:
        print("==> An exception getting service info")
        print(csr_const + csr.username)
        print(json_data_const + json.dumps(json_data['service_request']))
        return (None, ("Could not find service for service_id: " + str(service_request.service_id)), 400)

    if service.parent_id is None:
        print("==> CSR has selected a category, rather than a service.  This should not be possible")
        print(csr_const + csr.username)
        print("    --> Service:   " + service.service_name)
        return (None, "CSR has selected a category, rather than a service. Should not be possible", 400)

    return (service, "", 200)

@api.route("/service_requests/", methods=["POST"])
class ServiceRequestsList(Resource):

    citizen_schema = CitizenSchema()
    service_request_schema = ServiceReqSchema()

    @jwt.has_one_of_roles([Role.internal_user.value])
    @api_call_with_retry
    def post(self):
        try:
            json_data = request.get_json()
        except Exception as error:
            return {"message": str(error)}, 401

        csr = CSR.find_by_username(g.jwt_oidc_token_info['username'])
        service_request, message, code = get_service_request(self, json_data, csr)
        if (service_request is None):
            return {"message": message}, code

        active_sr_state = SRState.get_state_by_name("Active")
        complete_sr_state = SRState.get_state_by_name("Complete")

        citizen = None
        try:
            citizen = Citizen.query.get(service_request.citizen_id)
        except:
            print("==> An exception getting citizen info")
            print(csr_const + csr.username)
            print(json_data_const + json.dumps(json_data['service_request']))

        if citizen is None:
            return {"message": "No matching citizen found for citizen_id"}, 400

        service, message, code = get_service(service_request, json_data, csr)
        if (service is None):
            return {"message": message}, code

        # Find the currently active service_request and close it (if it exists)
        current_sr_number = 0
        for req in citizen.service_reqs:
            if req.sr_state_id == active_sr_state.sr_state_id:
                req.sr_state_id = complete_sr_state.sr_state_id
                req.finish_service(csr, clear_comments=False)
                current_sr_number = req.sr_number
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

            # Move start_time back 11 hours to account for DST and UTC offsets
            # tickets up till 10pm will not affect ticket numbering on next day
            offset_start_time = citizen.start_time - timedelta(hours=11)

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

        citizen.cs_id = active_id

        #  If first service, just choose it.  If additional service, more work needed.
        if len(citizen.service_reqs) == 0:
            snowplow_event = "chooseservice"
        else:
            snowplow_event = "additionalservice"

        service_request.sr_number = len(citizen.service_reqs) + 1

        db.session.add(service_request)
        db.session.add(citizen)
        db.session.commit()

        #  If first service, just need a choose service call.
        if snowplow_event == "chooseservice":
            SnowPlow.choose_service(service_request, csr, "chooseservice")

        #  If not first service, need stop service, choose service, and additional service calls.
        else:
            SnowPlow.snowplow_event(citizen.citizen_id, csr, "stopservice", current_sr_number=current_sr_number)
            SnowPlow.choose_service(service_request, csr, "chooseservice")
            SnowPlow.snowplow_event(citizen.citizen_id, csr, "additionalservice", current_sr_number=service_request.sr_number)

        citizen_result = self.citizen_schema.dump(citizen)
        socketio.emit('update_active_citizen', citizen_result, room=csr.office.office_name)
        result = self.service_request_schema.dump(service_request)

        return {'service_request': result,
                'errors': self.service_request_schema.validate(service_request)}, 201

try:
    citizen_state = CitizenState.query.filter_by(cs_state_name="Active").first()
    active_id = citizen_state.cs_id
except:
    active_id = 1
    print("==> In service_requests_list.py")
    print("    --> NOTE!!  You should only see this if doing a 'python3 manage.py db upgrade'")
