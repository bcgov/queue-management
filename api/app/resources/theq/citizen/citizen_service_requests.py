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
from flask import g
from flask_restx import Resource
from qsystem import api, my_print
from app.models.theq import Citizen, CSR
from app.schemas.theq import ServiceReqSchema
from sqlalchemy import exc
from app.utilities.auth_util import Role, has_any_role
from app.auth.auth import jwt


@api.route("/citizens/<int:id>/service_requests/", methods=["GET"])
class CitizenServiceRequests(Resource):

    service_requests_schema = ServiceReqSchema(many=True)

    @jwt.has_one_of_roles([Role.internal_user.value])
    def get(self, id):
        try:
            csr = CSR.find_by_username(g.jwt_oidc_token_info['username'])

            citizen = Citizen.query.filter_by(citizen_id=id, office_id=csr.office_id).first()
            my_print("==> GET /citizens/" + str(citizen.citizen_id) + '/service_requests/, Ticket: ' + citizen.ticket_number)
            result = self.service_requests_schema.dump(citizen.service_reqs)
            return {'service_requests': result,
                    'errors': self.service_requests_schema.validate(citizen.service_reqs)}

        except exc.SQLAlchemyError as exception:
            logging.exception(exception)
            return {'message': 'API is down'}, 500