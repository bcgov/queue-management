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
from qsystem import api, db
from sqlalchemy import exc
from app.models.theq import CSR, Office


@api.route("/offices/", methods=["GET"])
class OfficeList(Resource):

    def get(self):
        try:

            result = Office.get_all_active_offices()

            return {'offices': result,
                    'errors': {}}

        except exc.SQLAlchemyError as exception:
            logging.exception(exception)
            return {'message': 'API is down'}, 500
