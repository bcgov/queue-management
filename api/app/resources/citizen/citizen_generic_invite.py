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
from qsystem import api, api_call_with_retry, db, oidc
from app.models import CSR, CitizenState, Period, PeriodState, ServiceReq, SRState
from app.schemas import CitizenSchema


@api.route("/citizens/invite/", methods=['POST'])
class CitizenGenericInvite(Resource):

    citizen_schema = CitizenSchema()
    citizens_schema = CitizenSchema(many=True)

    @oidc.accept_token(require_token=True)
    @api_call_with_retry
    def post(self):

        csr = CSR.query.filter_by(username=g.oidc_token_info['username']).first()

        active_citizen_state = CitizenState.query.filter_by(cs_state_name='Active').first()
        waiting_period_state = PeriodState.query.filter_by(ps_name='Waiting').first()

        citizen = None

        if csr.qt_xn_csr_ind:
            period = Period.query.filter(Period.time_end.is_(None)) \
                .filter_by(ps_id=waiting_period_state.ps_id) \
                .join(Period.sr, aliased=True) \
                .join(ServiceReq.citizen, aliased=True) \
                .filter_by(qt_xn_citizen_ind=1,  cs_id=active_citizen_state.cs_id, office_id=csr.office_id) \
                .first()
        else:
            period = Period.query.filter(Period.time_end.is_(None)) \
                .filter_by(ps_id=waiting_period_state.ps_id) \
                .join(Period.sr, aliased=True) \
                .join(ServiceReq.citizen, aliased=True) \
                .filter_by(qt_xn_citizen_ind=0,  cs_id=active_citizen_state.cs_id, office_id=csr.office_id) \
                .first()

        if period is not None:
            citizen = period.sr.citizen

        # Either no quick txn citizens for the quick txn csr, or vice versa
        if citizen is None:
            print("3")
            period = Period.query.filter(Period.time_end.is_(None)) \
                .filter_by(ps_id=waiting_period_state.ps_id) \
                .join(Period.sr, aliased=True) \
                .join(ServiceReq.citizen, aliased=True) \
                .filter_by(cs_id=active_citizen_state.cs_id, office_id=csr.office_id) \
                .first()

            if period is not None:
                citizen = period.sr.citizen

        if citizen is None:
            return {"message": "There is no citizen to invite"}, 400

        active_service_request = citizen.get_active_service_request()
        active_service_request.invite(csr)

        pending_service_state = SRState.query.filter_by(sr_code='Pending').first()
        active_service_request.sr_state_id = pending_service_state.sr_state_id

        db.session.add(active_service_request)
        db.session.commit()

        result = self.citizen_schema.dump(citizen)
        return {'citizen': result.data,
                'errors': result.errors}, 200
