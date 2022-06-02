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

from flask_restx import Resource
from sqlalchemy import text, exc
from qsystem import api, db
sql = text('select 1')


@api.route("/healthz/")
class Healthz(Resource):

    @staticmethod
    def get():
        try:
            db.engine.execute(sql)
        except exc.SQLAlchemyError:
            return {"message": "api is down"}, 500

        # made it here, so all checks passed
        return {"message": "api is healthy"}, 200


@api.route("/readyz/")
class Readyz(Resource):

    @staticmethod
    def get():
        # add a poll to the DB when called
        return {"message": "api is ready"}, 200
