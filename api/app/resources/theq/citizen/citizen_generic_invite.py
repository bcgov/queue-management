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

from filelock import FileLock
from flask import g, request
from flask_restplus import Resource
from qsystem import api, api_call_with_retry, db, oidc, socketio
from app.models.theq import Citizen, CSR, CitizenState, Period, PeriodState, ServiceReq, SRState
from app.schemas.theq import CitizenSchema

@api.route("/citizens/invite/", methods=['POST'])
class CitizenGenericInvite(Resource):

    citizen_schema = CitizenSchema()
    citizens_schema = CitizenSchema(many=True)

    @oidc.accept_token(require_token=True)
    @api_call_with_retry
    def post(self):

        lock = FileLock("lock/invite_citizen.lock")

        with lock:
            csr = CSR.find_by_username(g.oidc_token_info['username'])

            active_citizen_state = CitizenState.query.filter_by(cs_state_name='Active').first()
            waiting_period_state = PeriodState.get_state_by_name("Waiting")
            citizen = None
            json_data = request.get_json()

            if json_data and 'counter_id' in json_data:
                counter_id = int(json_data.get('counter_id'))
            else:
                counter_id = int(csr.counter_id)

            citizen = Citizen.query \
                .filter_by(counter_id=counter_id, cs_id=active_citizen_state.cs_id, office_id=csr.office_id) \
                .join(Citizen.service_reqs) \
                .join(ServiceReq.periods) \
                .filter_by(ps_id=waiting_period_state.ps_id) \
                .filter(Period.time_end.is_(None)) \
                .order_by(Citizen.priority, Citizen.citizen_id) \
                .first()

            # If no matching citizen with the same counter type, get next one
            if citizen is None:
                citizen = Citizen.query \
                    .filter_by(cs_id=active_citizen_state.cs_id, office_id=csr.office_id) \
                    .join(Citizen.service_reqs) \
                    .join(ServiceReq.periods) \
                    .filter_by(ps_id=waiting_period_state.ps_id) \
                    .filter(Period.time_end.is_(None)) \
                    .order_by(Citizen.priority, Citizen.citizen_id) \
                    .first()

            if citizen is None:
                return {"message": "There is no citizen to invite"}, 400

            db.session.refresh(citizen)
            active_service_request = citizen.get_active_service_request()

            try:
                active_service_request.invite(csr, invite_type="generic", sr_count = len(citizen.service_reqs))
            except TypeError:
                return {"message": "Error inviting citizen. Please try again."}, 400

            active_service_state = SRState.get_state_by_name("Active")
            active_service_request.sr_state_id = active_service_state.sr_state_id

            db.session.add(citizen)
            db.session.commit()

            socketio.emit('update_customer_list', {}, room=csr.office_id)
            socketio.emit('citizen_invited', {}, room='sb-%s' % csr.office.office_number)
            result = self.citizen_schema.dump(citizen)
            socketio.emit('update_active_citizen', result.data, room=csr.office_id)

        return {'citizen': result.data,
                'errors': result.errors}, 200
