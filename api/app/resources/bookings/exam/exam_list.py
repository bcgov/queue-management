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
from flask import g, request
from flask_restplus import Resource
from sqlalchemy import exc
from app.models.bookings import Exam
from app.models.theq import CSR
from app.schemas.bookings import ExamSchema
from qsystem import api, oidc


@api.route("/exams/", methods=["GET"])
class ExamList(Resource):

    exam_schema = ExamSchema(many=True)

    @oidc.accept_token(require_token=True)
    def get(self):
        try:
            csr = CSR.find_by_username(g.oidc_token_info['username'])
            exams = Exam.query.filter(Exam.deleted_date.is_(None)).filter_by(office_id=csr.office_id)

            search_kwargs = {}

            if request.args:
                for key in request.args:
                    if hasattr(Exam, key):
                        search_kwargs[key] = request.args.get(key)

                exams = exams.filter_by(**search_kwargs)

            result = self.exam_schema.dump(exams)

            return {'exams': result.data,
                    'errors': result.errors}, 200

        except exc.SQLAlchemyError as error:
            logging.error(error, exc_info=True)
            return {"message": "api is down"}, 500
