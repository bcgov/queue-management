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
from flask_restplus import Resource
from qsystem import api, oidc
from app.models.theq import Citizen, CSR
from app.schemas.theq import ServiceReqSchema
from sqlalchemy import exc


@api.route("/citizens/<int:id>/service_requests/", methods=["GET"])
class CitizenServiceRequests(Resource):

    service_requests_schema = ServiceReqSchema(many=True)

    @oidc.accept_token(require_token=True)
    def get(self, id):
        try:
            csr = CSR.find_by_username(g.oidc_token_info['username'])

            citizen = Citizen.query.filter_by(citizen_id=id, office_id=csr.office_id).first()
            result = self.service_requests_schema.dump(citizen.service_reqs)
            return {'service_requests': result.data,
                    'errors': result.errors}

        except exc.SQLAlchemyError as e:
            print(e)
            return {'message': 'API is down'}, 500