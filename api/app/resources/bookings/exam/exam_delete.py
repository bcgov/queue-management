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

from datetime import datetime
from flask import g
from flask_restplus import Resource
from app.models.bookings import Exam
from app.models.theq import CSR
from app.schemas.bookings import ExamSchema
from qsystem import api, db, oidc


@api.route("/exams/<int:id>/", methods=["DELETE"])
class ExamDelete(Resource):

    exam_schema = ExamSchema()

    @oidc.accept_token(require_token=True)
    def delete(self, id):

        csr = CSR.find_by_username(g.oidc_token_info['username'])

        exam = Exam.query.filter_by(exam_id=id).first_or_404()

        if not (exam.office_id == csr.office_id or csr.role.role_code == "LIAISON"):
            return {"The Exam Office ID and CSR Office ID do not match!"}, 403

        exam.deleted_date = datetime.now()

        db.session.add(exam)
        db.session.commit()

        return {}, 204
