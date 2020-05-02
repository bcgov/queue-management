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
from app.schemas.bookings import ExamSchema
from qsystem import api, oidc
from app.utilities.auth_util import Role, has_any_role


@api.route("/exams/event_id/<int:id>/", methods=["GET"])
class ExamEventIDDetail(Resource):

    exam_schema = ExamSchema()

    @oidc.accept_token(require_token=True)
    @has_any_role(roles=[Role.internal_user.value])
    def get(self, id):

        try:
            exam = Exam.query.filter_by(event_id=str(id)).all()

            if not exam:
                return {'message': False}, 200

            else:
                return {'message': True}, 200

        except exc.SQLAlchemyError as error:

            logging.error(error, exc_info=True)
            return {"message": "API is down"}, 500
