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
from qsystem import api, api_call_with_retry, db, jwt, socketio
from app.models.theq import Citizen, CSR, CitizenState
from app.schemas.theq import CitizenSchema, ServiceReqSchema
from app.models.theq import SRState
from datetime import datetime
from app.utilities.snowplow import SnowPlow
import os

@api.route("/citizens/<int:id>/citizen_left/", methods=['POST'])
class CitizenLeft(Resource):

    service_request_schema = ServiceReqSchema(many=True)
    citizen_schema = CitizenSchema()
    clear_comments_flag = (os.getenv("THEQ_CLEAR_COMMENTS_FLAG", "True")).upper() == "TRUE"

    @jwt.requires_auth
    @api_call_with_retry
    def post(self, id):

        csr = CSR.find_by_username(g.jwt_oidc_token_info['preferred_username'])
        citizen = Citizen.query.filter_by(citizen_id=id, office_id=csr.office_id).first()
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

        SnowPlow.snowplow_event(citizen.citizen_id, csr, ("left/" + status),
                                quantity = quantity, current_sr_number= sr_number)

        for service_request in citizen.service_reqs:

            service_request.sr_state_id = sr_state.sr_state_id

            for p in service_request.periods:
                if p.time_end is None:
                    p.time_end = datetime.now()

            #  Make snowplow calls to finish any stopped services
            if service_request.sr_id != active_sr:
                SnowPlow.snowplow_event(citizen.citizen_id, csr, "finishstopped",
                                        quantity = service_request.quantity,
                                        current_sr_number= service_request.sr_number)

        citizen.cs = CitizenState.query.filter_by(cs_state_name='Left before receiving services').first()
        if self.clear_comments_flag:
            citizen.citizen_comments = None

        if citizen.start_time.date() != datetime.now().date():
            citizen.accurate_time_ind = 0

        db.session.add(citizen)
        db.session.commit()

        socketio.emit('citizen_invited', {}, room='sb-%s' % csr.office.office_number)
        result = self.citizen_schema.dump(citizen)
        socketio.emit('update_active_citizen', result.data, room=csr.office_id)

        return {'citizen': result.data,
                'errors': result.errors}, 200
