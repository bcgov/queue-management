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
from flask import request
from flask_restx import Resource
from sqlalchemy import exc, or_, desc
from app.models.bookings import Exam
from app.models.theq import CSR
from app.schemas.bookings import ExamSchema
from qsystem import api
from datetime import datetime, timedelta
from app.utilities.auth_util import Role, get_username
from app.auth.auth import jwt


@api.route("/exams/", methods=["GET"])
class ExamList(Resource):

    exam_schema = ExamSchema(many=True)

    @jwt.has_one_of_roles([Role.internal_user.value])
    def get(self):
        try:
            csr = CSR.find_by_username(get_username())

            ninety_day_filter = datetime.now() - timedelta(days=90)

            if csr.ita2_designate == 1:
                if request.args and request.args.get("office_number"):
                    exams = Exam.query.filter(Exam.deleted_date.is_(None)) \
                        .filter(or_(Exam.exam_returned_date.is_(None),
                                    Exam.exam_returned_date > ninety_day_filter)) \
                        .join(Exam.office, aliased=True) \
                        .filter_by(office_number=request.args.get("office_number")) \
                        .order_by(desc(Exam.exam_id))
                else:
                    exams = Exam.query.filter(Exam.deleted_date.is_(None)) \
                                      .filter(or_(Exam.exam_returned_date.is_(None),
                                                  Exam.exam_returned_date > ninety_day_filter)) \
                                      .order_by(desc(Exam.exam_id))

            else:
                exams = Exam.query.filter(Exam.deleted_date.is_(None))\
                                  .filter_by(office_id=csr.office_id)\
                                  .filter(or_(Exam.exam_returned_date.is_(None),
                                              Exam.exam_returned_date > ninety_day_filter))\
                                  .order_by(desc(Exam.exam_id))

            search_kwargs = {}

            if request.args:
                for key in request.args:
                    if hasattr(Exam, key):
                        search_kwargs[key] = request.args.get(key)

                exams = exams.filter_by(**search_kwargs)

            result = self.exam_schema.dump(exams)

            return {'exams': result,
                    'errors': self.exam_schema.validate(exams)}, 200

        except exc.SQLAlchemyError as error:
            logging.error(error, exc_info=True)
            return {"message": "api is down"}, 500
