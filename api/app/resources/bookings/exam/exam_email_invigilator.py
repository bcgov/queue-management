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

from flask import request
from flask_restx import Resource
import logging
from sqlalchemy import exc
from app.models.theq import CSR
from app.models.bookings import Exam
from app.utilities.auth_util import get_username
from app.utilities.bcmp_service import BCMPService
from qsystem import api, db
from app.auth.auth import jwt


@api.route("/exams/<int:exam_id>/email_invigilator/", methods=["POST"])
class ExamEmailInvigilator(Resource):
    bcmp_service = BCMPService()

    @jwt.requires_auth
    def post(self, exam_id):

        csr = CSR.find_by_username(get_username())

        try:
            exam = Exam.query.filter_by(exam_id=exam_id).first()

            if not (exam.office_id == csr.office_id or csr.ita2_designate == 1):
                return {"The Exam Office ID and CSR Office ID do not match!"}, 403

            json_data = request.get_json()
            invigilator_id = json_data["invigilator_id"]
            invigilator_name = json_data["invigilator_name"]
            invigilator_email = json_data["invigilator_email"]
            invigilator_phone = json_data["invigilator_phone"]

            if not invigilator_email or not invigilator_phone or not invigilator_name:
                return {"Invigilator name, email, and phone number are required"}, 422

            response = self.bcmp_service.email_exam_invigilator(
                exam,
                invigilator_name,
                invigilator_email,
                invigilator_phone
            )

            if response:
                exam.invigilator_id = invigilator_id
                db.session.add(exam)
                db.session.commit()
                return {}, 200
            else:
                return {}, 500

        except exc.SQLAlchemyError as error:
            logging.error(error, exc_info=True)
            return {'message': 'API is down'}, 500
