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

from flask import Response
from flask_restx import Resource
import io
import logging
import urllib
from werkzeug.wsgi import FileWrapper
from sqlalchemy import exc
from app.models.theq import CSR
from app.models.bookings import Exam
from app.utilities.auth_util import get_username
from app.utilities.bcmp_service import BCMPService
from qsystem import api, my_print
from app.auth.auth import jwt


@api.route("/exams/<int:exam_id>/download/", methods=["GET"])
class ExamStatus(Resource):
    bcmp_service = BCMPService()

    @jwt.requires_auth
    def get(self, exam_id):

        csr = CSR.find_by_username(get_username())

        try:
            exam = Exam.query.filter_by(exam_id=exam_id).first()

            if not (exam.office_id == csr.office_id or csr.ita2_designate == 1):
                return {"The Exam Office ID and CSR Office ID do not match!"}, 403

            job = self.bcmp_service.check_exam_status(exam)
            my_print(job)

            if job['jobStatus'] == 'PACKAGE_GENERATED':
                package_url = job["jobProperties"]["EXAM_PACKAGE_URL"]
                req = urllib.request.Request(package_url)
                response = urllib.request.urlopen(req).read()
                exam_file = io.BytesIO(response)
                file_wrapper = FileWrapper(exam_file)

                return Response(file_wrapper,
                                mimetype="application/pdf",
                                direct_passthrough=True,
                                headers={
                                    "Content-Disposition": 'attachment; filename="%s.csv"' % exam.exam_id,
                                    "Content-Type": "application/pdf"
                                })
            else:
                return {'message': 'Package not yet generated', 'status': job['jobStatus']}, 400

        except exc.SQLAlchemyError as error:
            logging.error(error, exc_info=True)
            return {'message': 'API is down'}, 500
