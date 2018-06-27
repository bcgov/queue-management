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
from app.models import ServiceReq, SRState
from app.schemas import CitizenSchema, ServiceReqSchema
from sqlalchemy import exc

@api.route("/citizens/<int:id>/service_requests/", methods=["GET"])
class CitizenServiceRequests(Resource):

    service_requests_schema = ServiceReqSchema(many=True)

    @oidc.accept_token(require_token=True)
    def get(self, id):
        try:
            csr = CSR.query.filter_by(username=g.oidc_token_info['username']).first()
            #csr = CSR.query.filter_by(username='adamkroon').first()
            citizen = Citizen.query.get(id)
            result = self.service_requests_schema.dump(citizen.service_reqs)
            return {'service_requests': result.data,
                    'errors': result.errors}

        except exc.SQLAlchemyError as e:
            print (e)
            return {'message': 'API is down'}, 500