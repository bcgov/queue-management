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
from qsystem import api, api_call_with_retry, db, oidc, socketio
from app.models import Citizen, CSR, CitizenState
from marshmallow import ValidationError
from app.schemas import CitizenSchema
from sqlalchemy import exc
from datetime import datetime
from ...utilities.snowplow import SnowPlow

@api.route("/citizens/", methods=['GET', 'POST'])
class CitizenList(Resource):

    citizen_schema = CitizenSchema()
    citizens_schema = CitizenSchema(many=True)

    @oidc.accept_token(require_token=True)
    def get(self):
        try:
            csr = CSR.find_by_username(g.oidc_token_info['username'])
            active_state = CitizenState.query.filter_by(cs_state_name="Active").first()
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
    @api_call_with_retry
    def post(self):
        json_data = request.get_json()

        csr = CSR.find_by_username(g.oidc_token_info['username'])

        try:
            citizen = self.citizen_schema.load(json_data).data
            citizen.office_id = csr.office_id
            citizen.start_time = datetime.now()

        except ValidationError as err:
            print(err)
            return {"message": err.messages}, 422

        citizen_state = CitizenState.query.filter_by(cs_state_name="Active").first()
        citizen.cs_id = citizen_state.cs_id
        citizen.service_count = 1
        db.session.add(citizen)
        db.session.commit()

        SnowPlow.add_citizen(citizen, csr)

        result = self.citizen_schema.dump(citizen)

        return {'citizen': result.data,
                'errors': result.errors}, 201
