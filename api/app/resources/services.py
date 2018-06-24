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
from app.models import Service
from app.models import Office
from cockroachdb.sqlalchemy import run_transaction
import logging
from sqlalchemy import exc
from app.schemas import ServiceSchema

@api.route("/services/", methods=["GET"])
class Services(Resource):

    service_schema = ServiceSchema(many=True)
    services_schema =  ServiceSchema(many=True)

    #@oidc.accept_token(require_token=True)
    def get(self):
        if request.args.get('office_id'):
            try:
                office_id = int(request.args['office_id'])
                office = Office.query.get(office_id)
                services = office.services
                result = self.service_schema.dump(services)
                return {'services': result.data,
                        'errors': result.errors}

            except exc.SQLAlchemyError as e:
                print (e)
                return {'message': 'API is down'}, 500

            except ValueError as e:
                return {'message': 'office_id must be an integer.'}, 400
        else:    
            try:
                services = Service.query.all()
                result = self.services_schema.dump(services)
                return {'services': result.data,
                        'errors': result.errors}

            except exc.SQLAlchemyError as e:
                print (e)
                return {'message': 'api is down'}, 500