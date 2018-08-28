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
from sqlalchemy import exc
from app.models import Citizen, CSR, Period, ServiceReq, SRState
from app.schemas import CitizenSchema, CSRSchema


@api.route("/csrs/me/", methods=["GET"])
class Services(Resource):

    csr_schema = CSRSchema()
    citizen_schema = CitizenSchema(many=True)

    @oidc.accept_token(require_token=True)
    def get(self):
        try:
            csr = CSR.query.filter_by(username=g.oidc_token_info['username'].split("idir/")[-1]).first()
            active_sr_state = SRState.query.filter_by(sr_code='Active').first()

            active_citizens = Citizen.query \
                .join(Citizen.service_reqs) \
                .filter_by(sr_state_id=active_sr_state.sr_state_id) \
                .join(ServiceReq.periods) \
                .filter_by(csr_id=csr.csr_id) \
                .filter(Period.time_end.is_(None))

            result = self.csr_schema.dump(csr)
            active_citizens = self.citizen_schema.dump(active_citizens)

            return {'csr': result.data,
                    'active_citizens': active_citizens.data,
                    'errors': result.errors}

        except exc.SQLAlchemyError as e:
            print(e)
            return {'message': 'API is down'}, 500
