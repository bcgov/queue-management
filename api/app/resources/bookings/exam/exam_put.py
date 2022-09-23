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
from flask import request, g
from flask_restx import Resource
from app.models.bookings import Exam
from app.models.theq import CSR
from app.schemas.bookings import ExamSchema
from qsystem import api, api_call_with_retry, db
from app.utilities.auth_util import Role, has_any_role
from app.auth.auth import jwt


@api.route("/exams/<int:id>/", methods=["PUT"])
class ExamPut(Resource):

    exam_schema = ExamSchema()

    @jwt.has_one_of_roles([Role.internal_user.value])
    @api_call_with_retry
    def put(self, id):

        csr = CSR.find_by_username(g.jwt_oidc_token_info['username'])
        json_data = request.get_json()

        if not json_data:
            return {"message": "No input data received for updating an exam"}

        # Deleted date filter original
        exam = Exam.query.filter_by(exam_id=id).first_or_404()

        if not (exam.office_id == csr.office_id or csr.ita2_designate == 1):
            return {"The Exam Office ID and CSR Office ID do not match!"}, 403

        exam = self.exam_schema.load(json_data, instance=exam, partial=True)
        warning = self.exam_schema.validate(json_data)

        if warning:
            logging.warning("WARNING: %s", warning)
            return {"message": warning}, 422

        db.session.add(exam)
        db.session.commit()

        result = self.exam_schema.dump(exam)

        return {"exam": result,
                "errors": self.exam_schema.validate(exam)}, 201
