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
from flask_restplus import Resource
from sqlalchemy import exc
from app.models.bookings import Invigilator
from app.models.theq import CSR
from app.schemas.bookings import InvigilatorSchema
from qsystem import api, oidc


@api.route("/invigilators/", methods=["GET"])
class InvigilatorList(Resource):

    invigilator_schema = InvigilatorSchema(many=True)

    @oidc.accept_token(require_token=True)
    def get(self):

        csr = CSR.find_by_username(g.oidc_token_info['username'])

        try:
            invigilators = Invigilator.query.filter_by(office_id=csr.office_id)
            result = self.invigilator_schema.dump(invigilators)
            return {'invigilators': result.data,
                    'errors': result.errors}, 200

        except exc.SQLAlchemyError as error:
            logging.error(error, exc_info=True)
            return {"message": "api is down"}, 500
