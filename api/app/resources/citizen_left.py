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

from flask import request, jsonify, g
from flask_restplus import Resource
from qsystem import api, db, oidc, socketio
from app.auth import required_scope
from app.models import Citizen, CSR, CitizenState
from cockroachdb.sqlalchemy import run_transaction
import logging
from marshmallow import ValidationError, pre_load
from app.schemas import CitizenSchema, ServiceReqSchema
from app.models import CitizenState, SRState, Service
from sqlalchemy import exc

@api.route("/citizens/<int:id>/citizen_left/", methods=['POST'])
class CitizenLeft(Resource):

    service_request_schema = ServiceReqSchema(many=True)
    citizen_schema = CitizenSchema()

    #@oidc.accept_token(require_token=True)
    def post(self, id):
        json_data = request.get_json()
        
        #csr = CSR.query.filter_by(username=g.oidc_token_info['username']).first()
        csr = CSR.query.filter_by(username='adamkroon').first()
        citizen = Citizen.query.get(id) 

        sr_state = SRState.query.filter_by(sr_code="Complete").first()

        for service_request in citizen.service_reqs:

            service_request.sr_state_id = sr_state.sr_state_id

            for p in service_request.periods:
                if p.end_time is None:
                    p.end_time = datetime.now()
                    
                    db.session.add(p)

        citizen.citizen_state = CitizenState.query.filter_by(cs_state_name='Left before receiving services').first()
        
        db.session.add(service_request)
        db.session.commit()
        result = self.citizen_schema.dump(citizen)

        return {'citizen': result.data,
                'errors': result.errors}, 201
