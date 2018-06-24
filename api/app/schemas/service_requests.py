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
from app.models import ServiceReq
from app.models import Citizen
from cockroachdb.sqlalchemy import run_transaction
import logging
from sqlalchemy import exc
from app.schemas import ServiceReqSchema

@api.route("/services_requests/", methods=["GET", "POST", "PUT"])
class ServiceRequests(Resource):

    service_requests_schema = ServiceRequestSchema(many=True)

    #@oidc.accept_token(require_token=True)
    def get(self):
        try:
            csr = CSR.query.filter_by(username=g.oidc_token_info['username']).first()
            citizens = Citizen.query.filter_by(office_id=csr.office_id).all()
            result = self.citizens_schema.dump(citizens)
            return {'citizens': result.data,
                    'errors': result.errors}, 200

        except exc.SQLAlchemyError as e:
            print (e)
            return {'message': 'API is down'}, 500


    #@oidc.accept_token(require_token=True)
    def post(self):
        json_data = request.get_json()

        if not json_data:
            return {"message": "No input data received for creating citizen"}, 400
        
        csr = CSR.query.filter_by(username=g.oidc_token_info['username']).first()

        try:
            data = self.service_requests_schema.load(json_data).data

        except ValidationError as err:
            return {"message": err.messages}, 422

        # DO WORK HERE
        citizen = 

        return {"message": "Service Request successfully created."}, 201