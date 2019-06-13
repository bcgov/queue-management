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

from flask import g, request
from flask_restplus import Resource
from qsystem import api, api_call_with_retry, db, oidc, socketio, my_print
from app.models.theq import Citizen, CSR, CitizenState
from app.models.theq import SRState
from app.schemas.theq import CitizenSchema
from app.utilities.snowplow import SnowPlow
from datetime import datetime
import os

@api.route("/citizens/<int:id>/finish_service/", methods=["POST"])
class CitizenFinishService(Resource):

    citizen_schema = CitizenSchema()
    clear_comments_flag = (os.getenv("THEQ_CLEAR_COMMENTS_FLAG", "True")).upper() == "TRUE"

    @oidc.accept_token(require_token=True)
    @api_call_with_retry
    def post(self, id):
        csr = CSR.find_by_username(g.oidc_token_info['username'])
        citizen = Citizen.query.filter_by(citizen_id=id, office_id=csr.office_id).first()
        my_print("==> POST /citizens/" + str(citizen.citizen_id) + '/finish_service/, Ticket: ' + citizen.ticket_number)
        active_service_request = citizen.get_active_service_request()
        inaccurate = request.args.get('inaccurate')

        if active_service_request is None:
            return {"message": "Citizen has no active service requests"}

        #  If citizen here overnight, or inaccurate time flag set, update accurate time flag.
        if citizen.start_time.date() != datetime.now().date() or inaccurate == 'true':
            citizen.accurate_time_ind = 0

        SnowPlow.snowplow_event(citizen.citizen_id, csr, "finish",
                                quantity = active_service_request.quantity,
                                current_sr_number= active_service_request.sr_number)

        active_sr_id = active_service_request.sr_id
        active_service_request.finish_service(csr, self.clear_comments_flag)
        citizen_state = CitizenState.query.filter_by(cs_state_name="Received Services").first()
        citizen.cs_id = citizen_state.cs_id

        pending_service_state = SRState.get_state_by_name("Complete")
        active_service_request.sr_state_id = pending_service_state.sr_state_id

        db.session.add(citizen)
        db.session.commit()

        #  Loop to stop all services in the service stopped state (which are all except the active service)
        if len(citizen.service_reqs) != 1:
            for sr in citizen.service_reqs:
                if sr.sr_id != active_sr_id:
                    SnowPlow.snowplow_event(citizen.citizen_id, csr, "finishstopped",
                                            quantity = sr.quantity,
                                            current_sr_number= sr.sr_number)

        socketio.emit('citizen_invited', {}, room='sb-%s' % csr.office.office_number)
        result = self.citizen_schema.dump(citizen)
        socketio.emit('update_active_citizen', result.data, room=csr.office_id)

        return {'citizen': result.data,
                'errors': result.errors}, 200
