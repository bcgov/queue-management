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
import logging
from sqlalchemy import exc
from app.models.theq import CSR
from app.models.bookings import Exam
from app.utilities.auth_util import get_username
from app.utilities.document_service import DocumentService
from qsystem import api, application
from app.auth.auth import jwt


@api.route("/exams/<int:exam_id>/upload/", methods=["GET"])
class ExamStatus(Resource):

    @jwt.requires_auth
    def get(self, exam_id):
        csr = CSR.find_by_username(get_username())

        try:
            exam = Exam.query.filter_by(exam_id=exam_id).first()

            if not (exam.office_id == csr.office_id or csr.ita2_designate == 1):
                return {"The Exam Office ID and CSR Office ID do not match!"}, 403
            client = DocumentService(
                application.config["MINIO_HOST"],
                application.config["MINIO_BUCKET"],
                application.config["MINIO_ACCESS_KEY"],
                application.config["MINIO_SECRET_KEY"],
                application.config["MINIO_USE_SECURE"]
            )

            object_name = "%s.pdf" % exam_id
            url = client.get_presigned_put_url(object_name)

            return {"url": url}

        except exc.SQLAlchemyError as error:
            logging.error(error, exc_info=True)
            return {'message': 'API is down'}, 500
