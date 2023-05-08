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
from sqlalchemy import exc
from app.models.bookings import Exam
from app.models.theq import CSR
from app.schemas.bookings import ExamSchema
from qsystem import api
from app.utilities.auth_util import Role, get_username
from app.auth.auth import jwt


@api.route("/exams/<int:id>/", methods=["GET"])
class ExamDetail(Resource):

    exam_schema = ExamSchema()

    @jwt.has_one_of_roles([Role.internal_user.value])
    def get(self, id):

        csr = CSR.find_by_username(get_username())

        try:
            exam = Exam.query.filter_by(exam_id=id).first()

            if not (exam.office_id == csr.office_id or csr.ita2_designate == 1):
                return {"The Exam Office ID and CSR Office ID do not match!"}, 403

            result = self.exam_schema.dump(exam)
            return {'exam': result,
                    'errors': self.exam_schema.validate(exam)}, 200

        except exc.SQLAlchemyError as error:
            logging.error(error, exc_info=True)
            return {'message': 'API is down'}, 500
