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
from flask_restx import Resource
from qsystem import api, db, oidc, time_print, get_key
from sqlalchemy import exc
from app.models.theq import CSRState
from app.schemas.theq import CSRStateSchema
from app.utilities.auth_util import Role, has_any_role, has_role


@api.route("/csr_states/", methods=["GET"])
class CsrStateList(Resource):

    csr_state_schema = CSRStateSchema(many=True, exclude=('csrs'))

    @oidc.accept_token(require_token=True)
    def get(self):
        try:
            user = g.oidc_token_info['username']
            has_role([Role.internal_user.value], g.oidc_token_info['realm_access']['roles'], user, "CsrStateList GET /csr_states/")
            states = CSRState.query.all()
            result = self.csr_state_schema.dump(states)

            return {'csr_states': result.data,
                    'errors': result.errors}

        except exc.SQLAlchemyError as e:
            print(e)
            return {'message': 'API is down'}, 500
