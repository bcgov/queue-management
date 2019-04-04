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
from qsystem import api, db, jwt
from sqlalchemy import exc
from app.models.theq import CSR, Office
from app.schemas.theq import OfficeSchema


@api.route("/offices/", methods=["GET"])
class OfficeList(Resource):

    office_schema = OfficeSchema(many=True)

    @jwt.requires_auth
    def get(self):
        try:

            offices = Office.query.filter(Office.deleted.is_(None))
            result = self.office_schema.dump(offices)

            return {'offices': result.data,
                    'errors': result.errors}

        except exc.SQLAlchemyError as e:
            print(e)
            return {'message': 'API is down'}, 500
