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

import logging
from flask import request, g
from flask_restx import Resource
from qsystem import api, api_call_with_retry, db, socketio, get_key
from app.models.theq import Citizen, CSR, CitizenState, Period, ServiceReq, citizen
from marshmallow import ValidationError
from app.schemas.theq import CitizenSchema
from sqlalchemy import exc
from datetime import datetime
from app.utilities.snowplow import SnowPlow
from app.utilities.auth_util import Role, get_username, has_role
from app.auth.auth import jwt
from sqlalchemy.orm import raiseload, joinedload
from sqlalchemy.dialects import postgresql

@api.route("/citizens/", methods=['GET'])
class CitizenList(Resource):

    citizen_schema = CitizenSchema()
    citizens_schema = CitizenSchema(many=True)

    @jwt.requires_auth
    def get(self):
        try:
            username = get_username()
            has_role([Role.internal_user.value], g.jwt_oidc_token_info['realm_access']['roles'], username, "CitizenList GET /citizens/")
            csr = CSR.find_by_username(username)
            if not csr:
                db.session.close()
                raise Exception('no user found with username: `{}`'.format(username))

            citizens = Citizen.query \
                .options(joinedload(Citizen.service_reqs, innerjoin=True).joinedload(ServiceReq.periods).options(raiseload(Period.sr),joinedload(Period.csr).raiseload('*')),raiseload(Citizen.office),raiseload(Citizen.counter),raiseload(Citizen.user)) \
                .filter_by(office_id=csr.office_id, cs_id=active_id) \
                .order_by(Citizen.priority)

            result = self.citizens_schema.dump(citizens)
            return {'citizens': result,
                    'errors': self.citizens_schema.validate(citizens)}, 200

        except exc.SQLAlchemyError as exception:
            logging.exception(exception)
            return {'message': 'API is down'}, 500

@api.route("/citizens/<int:citizens_waiting>/add_citizen/", methods=['POST'])
class CitizenList(Resource):
    citizen_schema = CitizenSchema()
    citizens_schema = CitizenSchema(many=True)

    @jwt.has_one_of_roles([Role.internal_user.value])
    @api_call_with_retry
    def post(self, citizens_waiting):

        username = get_username()
        has_role([Role.internal_user.value], g.jwt_oidc_token_info['realm_access']['roles'], username,
                 "CitizenList POST /citizens/")

        json_data = request.get_json()

        csr = CSR.find_by_username(username)
        if not csr:
            db.session.close()
            raise Exception('no user found with username: `{}`'.format(username))

        try:

            if not json_data:
                json_data = {}
            citizen = self.citizen_schema.load(json_data)
            citizen.office_id = csr.office_id
            citizen.start_time = datetime.utcnow()
            citizen.start_position = citizens_waiting + 1

        except ValidationError as err:
            logging.exception(err)
            return {"message": err.messages}, 422

        citizen.cs_id = active_id
        citizen.service_count = 1
        db.session.add(citizen)
        db.session.commit()

        SnowPlow.add_citizen(citizen, csr)

        result = self.citizen_schema.dump(citizen)

        return {'citizen': result,
                'errors': self.citizen_schema.validate(citizen)}, 201

try:
    key = get_key()
    citizen_state = CitizenState.query.filter_by(cs_state_name="Active").first()
    active_id = citizen_state.cs_id
except:
    active_id = 1
    logging.exception("==> In citizen_list.py")
    logging.exception("    --> NOTE!!  You should only see this if doing a 'python3 manage.py db upgrade'")
