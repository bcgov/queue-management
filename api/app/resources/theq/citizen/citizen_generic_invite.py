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

from filelock import FileLock
from flask import g, request
from flask_restx import Resource
from qsystem import api, api_call_with_retry, db, oidc, socketio, my_print
from app.models.theq import Citizen, CSR, CitizenState, Period, PeriodState, ServiceReq, SRState
from app.schemas.theq import CitizenSchema

@api.route("/citizens/invitetest/", methods=['POST'])
class CitizenGenericInvite(Resource):

    citizen_schema = CitizenSchema()
    citizens_schema = CitizenSchema(many=True)

    @oidc.accept_token(require_token=True)
    @api_call_with_retry
    def post(self):

        return {'citizen': "None",
                'errors': "None"}, 200
