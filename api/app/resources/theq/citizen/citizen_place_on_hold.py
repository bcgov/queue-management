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
from flask_restx import Resource
from app.models.theq.office import Office
from app.models.theq.service import Service
from qsystem import api, api_call_with_retry, db, socketio, my_print
from app.models.theq import Citizen, CSR, ServiceReq, Period
from app.models.theq import SRState
from app.schemas.theq import CitizenSchema
from app.utilities.auth_util import Role, has_any_role
from app.auth.auth import jwt
from sqlalchemy.orm import raiseload, joinedload
from sqlalchemy.dialects import postgresql

@api.route("/citizens/<int:id>/place_on_hold/", methods=["POST"])
class CitizenPlaceOnHold(Resource):

    citizen_schema = CitizenSchema()

    @jwt.has_one_of_roles([Role.internal_user.value])
    @api_call_with_retry
    def post(self, id):
        csr = CSR.find_by_username(g.jwt_oidc_token_info['username'])

        citizen = Citizen.query\
        .options(joinedload(Citizen.service_reqs, innerjoin=True).joinedload(ServiceReq.periods, innerjoin=True).options(raiseload(Period.sr),joinedload(Period.csr, innerjoin=True).raiseload('*')),joinedload(Citizen.office),raiseload(Citizen.user)) \
        .filter_by(citizen_id=id, office_id=csr.office_id)
        print('***** citizen_place_on_hold.py opt query: *****')
        print(str(citizen.statement.compile(dialect=postgresql.dialect())))
        citizen = citizen.first()


        my_print("==> POST /citizens/" + str(citizen.citizen_id) + '/place_on_hold/, Ticket: ' + citizen.ticket_number)
        active_service_request = citizen.get_active_service_request()

        if active_service_request is None:
            return {"message": "Citizen has no active service requests"}

        active_service_request.place_on_hold(csr)
        pending_service_state = SRState.get_state_by_name("Active")
        active_service_request.sr_state_id = pending_service_state.sr_state_id

        db.session.add(citizen)
        db.session.commit()

        socketio.emit('update_customer_list', {}, room=csr.office.office_name)
        result = self.citizen_schema.dump(citizen)
        socketio.emit('update_active_citizen', result, room=csr.office.office_name)

        return {'citizen': result,
                'errors': self.citizen_schema.validate(citizen)}, 200
