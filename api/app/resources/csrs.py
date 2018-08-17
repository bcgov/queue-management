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

from flask import request, g
from flask_restplus import Resource
from qsystem import api, oidc
from sqlalchemy import exc
from app.models import CSR
from app.schemas import CSRSchema


@api.route("/csrs/me/", methods=["GET"])
class Services(Resource):

    csr_schema = CSRSchema()

    @oidc.accept_token(require_token=True)
    def get(self):
        try:
            print (g.oidc_token_info)
            csr = CSR.query.filter_by(username=g.oidc_token_info['username'].split("idir/")[-1]).first()
            result = self.csr_schema.dump(csr)

            return {'csr': result.data,
                    'errors': result.errors}

        except exc.SQLAlchemyError as e:
            print(e)
            return {'message': 'API is down'}, 500
