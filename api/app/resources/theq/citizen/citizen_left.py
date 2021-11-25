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
from app.models.theq.office import Office
from qsystem import api, api_call_with_retry, db, socketio, my_print
from app.models.theq import Citizen, CSR, CitizenState, ServiceReq, Period, Service, Office
from app.schemas.theq import CitizenSchema, ServiceReqSchema
from app.models.theq import SRState
from datetime import datetime
from app.utilities.snowplow import SnowPlow
import os
from app.utilities.auth_util import Role, has_any_role
from app.auth.auth import jwt
from sqlalchemy.orm import raiseload, joinedload
from sqlalchemy.dialects import postgresql


@api.route("/citizens/<int:id>/citizen_left/", methods=['POST'])
class CitizenLeft(Resource):

    service_request_schema = ServiceReqSchema(many=True)
    citizen_schema = CitizenSchema()
    clear_comments_flag = (os.getenv("THEQ_CLEAR_COMMENTS_FLAG", "True")).upper() == "TRUE"

    @jwt.has_one_of_roles([Role.internal_user.value])
    @api_call_with_retry
    def post(self, id):

        my_print("++> POST API call time before csr = statement: " + str(datetime.now()))
        csr = CSR.find_by_username(g.jwt_oidc_token_info['username'])
        my_print("    ++> Time before citizen = statement: " + str(datetime.now()))

        citizen = Citizen.query\
            .options(joinedload(Citizen.service_reqs, innerjoin=True).joinedload(ServiceReq.periods, innerjoin=True).options(raiseload(Period.sr),joinedload(Period.csr, innerjoin=True).raiseload('*')),joinedload(Citizen.office),raiseload(Citizen.user)) \
            .filter_by(citizen_id=id)

        print('***** citizen_left.py opt query: *****')
        print(str(citizen.statement.compile(dialect=postgresql.dialect())))

        citizen = citizen.first()

        my_print("    ++> Time before citizen ID statement: " + str(datetime.now()))
        citizen_id_string = self.get_citizen_string(citizen)
        citizen_ticket = self.get_ticket_string(citizen)

        my_print("    ++> Time before citizen ticket statement: " + str(datetime.now()))
        my_print("    ++> POST /citizens/" + citizen_id_string + '/citizen_left/, Ticket: ' + citizen_ticket)
        my_print("    ++> Time before sr_state statement: " + str(datetime.now()))
        sr_state = SRState.get_state_by_name("Complete")

        #  Create parameters for and make snowplow call.  Default is no service request, CSR pressed cancel.
        quantity = 0
        sr_number = 1
        active_sr = 0
        status = "service-creation"
        if len(citizen.service_reqs) != 0:
            active_service_request = citizen.get_active_service_request()
            quantity = active_service_request.quantity
            sr_number = active_service_request.sr_number
            active_sr = active_service_request.sr_id
            active_period = active_service_request.get_active_period()
            if active_period.ps.ps_name == "Invited":
                status = "at-prep"
            else:
                status = "being-served"

        my_print("    ++> Time before Snowplow call: " + str(datetime.now()))
        SnowPlow.snowplow_event(citizen.citizen_id, csr, ("left/" + status),
                                quantity = quantity, current_sr_number= sr_number)

        my_print("    ++> Time before closing non-active service requests: " + str(datetime.now()))
        for service_request in citizen.service_reqs:

            service_request.sr_state_id = sr_state.sr_state_id

            for p in service_request.periods:
                if p.time_end is None:
                    p.time_end = datetime.utcnow()

            #  Make snowplow calls to finish any stopped services
            if service_request.sr_id != active_sr:
                SnowPlow.snowplow_event(citizen.citizen_id, csr, "finishstopped",
                                        quantity = service_request.quantity,
                                        current_sr_number= service_request.sr_number)

        my_print("    ++> Time before updating citizen state: " + str(datetime.now()))
        citizen.cs = CitizenState.query.filter_by(cs_state_name='Left before receiving services').first()
        if self.clear_comments_flag:
            citizen.citizen_comments = None
        if citizen.start_time.date() != datetime.now().date():
            citizen.accurate_time_ind = 0

        # remove walkin unique id when, citizen leave
        citizen.walkin_unique_id = None
        my_print("    ++> Time before updating citizen database: " + str(datetime.now()))
        db.session.add(citizen)
        my_print("    ++> Time before database commit: " + str(datetime.now()))
        db.session.commit()

        my_print("    ++> Time before socket io invited call: " + str(datetime.now()))
        socketio.emit('citizen_invited', {}, room='sb-%s' % csr.office.office_number)
        my_print("    ++> Time before creating the result: " + str(datetime.now()))
        result = self.citizen_schema.dump(citizen)
        my_print("    ++> Time before socket io update call: " + str(datetime.now()))
        socketio.emit('update_active_citizen', result, room=csr.office.office_name)

        my_print("    ++> Time before return result call: " + str(datetime.now()))
        return {'citizen': result,
                'errors': self.citizen_schema.validate(citizen)}, 200

    def get_citizen_string(self, citizen):
        if citizen is not None:
            if citizen.citizen_id is not None:
                citizen_id_string = str(citizen.citizen_id)
            else:
                citizen_id_string = "No ID"
        else:
            citizen_id_string = "No citizen"
        return citizen_id_string

    def get_ticket_string(self, citizen):
        if citizen is not None:
            if citizen.ticket_number is not None:
                citizen_ticket = citizen.ticket_number
            else:
                citizen_ticket = "None"
        else:
            citizen_ticket = "No citizen"
        return citizen_ticket
