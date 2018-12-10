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

from functools import cmp_to_key
from flask import request
from flask_restplus import Resource
from qsystem import api, oidc
from app.models.theq import Service
from app.models.theq import Office
from sqlalchemy import exc
from app.schemas.theq import ServiceSchema


@api.route("/services/", methods=["GET"])
class Services(Resource):

    service_schema = ServiceSchema(many=True)
    services_schema = ServiceSchema(many=True)

    @classmethod
    def sort_services(cls, a, b):
        if a.parent is None and b.parent is not None:
            return -1
        elif a.parent is not None and b.parent is None:
            return 1
        elif (a.parent is None and b.parent is None) or (a.parent == b.parent):
            if a.service_name.lower() < b.service_name.lower():
                return -1
            else:
                return 1
        else:
            if a.parent.service_name.lower() < b.parent.service_name.lower():
                return -1
            else:
                return 1

    @oidc.accept_token(require_token=True)
    def get(self):
        if request.args.get('office_id'):
            try:
                office_id = int(request.args['office_id'])
                office = Office.query.get(office_id)
                services = sorted(office.services, key=cmp_to_key(self.sort_services))
                filtered_services = [s for s in services if s.deleted is None]
                result = self.service_schema.dump(filtered_services)
                
                return {'services': result.data,
                        'errors': result.errors}

            except exc.SQLAlchemyError as e:
                print(e)
                return {'message': 'API is down'}, 500

            except ValueError as e:
                return {'message': 'office_id must be an integer.'}, 400
        else:
            try:
                services = Service.query.filter_by(actual_service_ind=1).all()
                result = self.services_schema.dump(services)
                return {'services': result.data,
                        'errors': result.errors}

            except exc.SQLAlchemyError as e:
                print(e)
                return {'message': 'api is down'}, 500
