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
from flask_restx import Resource
from sqlalchemy import exc,asc
from app.models.bookings import ExamType
from app.schemas.bookings import ExamTypeSchema
from qsystem import api
from app.utilities.auth_util import Role, has_any_role
from app.auth.auth import jwt


@api.route("/exam_types/", methods=["GET"])
class ExamTypeList(Resource):

    exam_type_schema = ExamTypeSchema(many=True)

    @jwt.has_one_of_roles([Role.internal_user.value])
    def get(self):

        try:
            exam_types = ExamType.query.filter(ExamType.deleted.is_(None)).order_by(asc(ExamType.exam_type_name))
            result = self.exam_type_schema.dump(exam_types)
            return {'exam_types': result,
                    'errors': self.exam_type_schema.validate(exam_types)}, 200

        except exc.SQLAlchemyError as error:
            logging.error(error, exc_info=True)
            return {'message': 'API is down'}, 500
