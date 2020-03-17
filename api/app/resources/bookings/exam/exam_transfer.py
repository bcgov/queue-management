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
import logging
from sqlalchemy import exc
from app.models.theq import CSR
from app.models.bookings import Exam
from app.utilities.bcmp_service import BCMPService
from qsystem import api, oidc


@api.route("/exams/<int:exam_id>/transfer/", methods=["POST"])
class ExamStatus(Resource):
    bcmp_service = BCMPService()

    @oidc.accept_token(require_token=True)
    def post(self, exam_id):

        csr = CSR.find_by_username(g.oidc_token_info['username'])

        try:
            exam = Exam.query.filter_by(exam_id=exam_id).first()

            if not (exam.office_id == csr.office_id or csr.liaison_designate == 1):
                return {"The Exam Office ID and CSR Office ID do not match!"}, 403

            self.bcmp_service.send_exam_to_bcmp(exam)
            return {}

        except exc.SQLAlchemyError as error:
            logging.error(error, exc_info=True)
            return {'message': 'API is down'}, 500
