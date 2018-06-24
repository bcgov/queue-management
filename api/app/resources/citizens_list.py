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
import sqlalchemy.orm
from qsystem import api, db, oidc, socketio
from app.auth import required_scope
from app.models import Citizen, CSR, CitizenState
from cockroachdb.sqlalchemy import run_transaction
import logging
from marshmallow import ValidationError, pre_load
from app.schemas import CitizenSchema
from sqlalchemy import exc
from sqlalchemy.orm import scoped_session, sessionmaker

@api.route("/citizens/", methods=['GET', 'POST'])
class CitizenList(Resource):

    citizen_schema = CitizenSchema()
    citizens_schema = CitizenSchema(many=True)

    #@oidc.accept_token(require_token=True)
    def get(self):
        try:
            #csr = CSR.query.filter_by(username=g.oidc_token_info['username']).first()
            csr = CSR.query.filter_by(username='adamkroon').first()
            citizens = Citizen.query.filter_by(office_id=csr.office_id).all()
            result = self.citizens_schema.dump(citizens)
            return {'citizens': result.data,
                    'errors': result.errors}, 200

        except exc.SQLAlchemyError as e:
            print (e)
            return {'message': 'API is down'}, 500

    #@oidc.accept_token(require_token=True)
    def post(self):
        Session = scoped_session(sessionmaker(bind=db.engine))

        json_data = request.get_json()
        
        #csr = CSR.query.filter_by(username=g.oidc_token_info['username']).first()
        csr = CSR.query.filter_by(username='adamkroon').first()

        try:
           citizen = self.citizen_schema.load(json_data, session=Session).data
           citizen.office_id = csr.office_id

        except ValidationError as err:
            print (err)
            return {"message": err.messages}, 422

        citizen_state = CitizenState.query.filter_by(cs_state_name="Active").first()
        citizen.cs_id = citizen_state.cs_id
        citizen.save()

        return {'message': 'Citizen successfully created.'}, 201

