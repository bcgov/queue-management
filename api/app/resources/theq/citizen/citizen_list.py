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
from qsystem import api, api_call_with_retry, db, oidc, socketio, time_print, get_key
from app.models.theq import Citizen, CSR, CitizenState
from marshmallow import ValidationError
from app.schemas.theq import CitizenSchema
from sqlalchemy import exc
from datetime import datetime
from app.utilities.snowplow import SnowPlow
from app.utilities.auth_util import Role, has_any_role

@api.route("/citizens/", methods=['GET', 'POST'])
class CitizenList(Resource):

    citizen_schema = CitizenSchema()
    citizens_schema = CitizenSchema(many=True)

    @oidc.accept_token(require_token=True)
    @has_any_role(roles=[Role.internal_user.value])
    def get(self):
        try:
            user = g.oidc_token_info['username']
            key = get_key()
            time_print("==> K<" + key + "> In CitizenList get, before csr call, user: " + user)
            csr = CSR.find_by_username(g.oidc_token_info['username'])
            time_print("--> K<" + key + "> In CitizenList get, after  csr call, user: " + user)
            if not csr:
                raise Exception('no user found with username: `{}`'.format(g.oidc_token_info['username']))
            time_print("==> K<" + key + "> In CitizenList get, before active call, user: " + user)
            active_state = CitizenState.query.filter_by(cs_state_name="Active").first()
            time_print("--> K<" + key + "> In CitizenList get, after  active call, cs_id: " + str(active_state.cs_id) + "; active_id: " + str(active_id))
            citizens = Citizen.query.filter_by(office_id=csr.office_id, cs_id=active_state.cs_id) \
                .order_by(Citizen.priority) \
                .join(Citizen.service_reqs).all()
            result = self.citizens_schema.dump(citizens)
            return {'citizens': result.data,
                    'errors': result.errors}, 200

        except exc.SQLAlchemyError as e:
            print(e)
            return {'message': 'API is down'}, 500

    @oidc.accept_token(require_token=True)
    @has_any_role(roles=[Role.internal_user.value])
    @api_call_with_retry
    def post(self):

        user = g.oidc_token_info['username']
        key = get_key()

        json_data = request.get_json()

        time_print("==> K<" + key + "> In CitizenList post, before csr call, user: " + user)
        csr = CSR.find_by_username(g.oidc_token_info['username'])
        time_print("--> K<" + key + "> In CitizenList post, after  csr call, user: " + user)
        if not csr:
            raise Exception('no user found with username: `{}`'.format(g.oidc_token_info['username']))

        try:
            citizen = self.citizen_schema.load(json_data).data
            citizen.office_id = csr.office_id
            citizen.start_time = datetime.now()

        except ValidationError as err:
            print(err)
            return {"message": err.messages}, 422

        citizen.cs_id = active_id
        citizen.service_count = 1
        db.session.add(citizen)
        db.session.commit()

        SnowPlow.add_citizen(citizen, csr)

        result = self.citizen_schema.dump(citizen)

        return {'citizen': result.data,
                'errors': result.errors}, 201

try:
    key = get_key()
    user = 'Startup'
    time_print("==> K<" + key + "> In CitizenList startup, before call, user: " + user)
    citizen_state = CitizenState.query.filter_by(cs_state_name="Active").first()
    time_print("--> K<" + key + "> In CitizenList startup, after  call, user: " + user)
    active_id = citizen_state.cs_id
except:
    active_id = 1
    print("==> In citizen_list.py")
    print("    --> NOTE!!  You should only see this if doing a 'python3 manage.py db upgrade'")
