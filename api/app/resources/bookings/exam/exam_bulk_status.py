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
import json
from flask import g
from flask_restx import Resource
from sqlalchemy import exc
from app.models.bookings import Exam
from app.schemas.bookings import ExamSchema
from app.models.theq import CSR
from app.utilities.bcmp_service import BCMPService
from qsystem import api, db, my_print
from app.auth.auth import jwt


@api.route("/exams/bcmp_status/", methods=["POST"])
class ExamList(Resource):
    bcmp_service = BCMPService()
    exam_schema = ExamSchema()

    @jwt.requires_auth
    def post(self):

        try:
            exams = Exam.query.filter_by(upload_received_ind=0).filter(Exam.bcmp_job_id.isnot(None))
            bcmp_response = self.bcmp_service.bulk_check_exam_status(exams)

            job_ids = []
            for job in bcmp_response["jobs"]:
                if job["jobStatus"] == "RESPONSE_UPLOADED":
                    job_ids.append(job["jobId"])

            my_print("job_ids to update: ")
            my_print(job_ids)

            exams_tobe_updated = None

            if len(job_ids) != 0:
                exams_tobe_updated = Exam.query.filter(Exam.bcmp_job_id.in_(job_ids))

                for exam in exams_tobe_updated:
                    exam_upd = self.exam_schema.load({'upload_received_ind': 1}, instance=exam, partial=True)
                    db.session.add(exam_upd)

                try:
                    db.session.commit()
                except:
                    db.session.rollback()
                    raise

            return {"exams_updated": exams_tobe_updated}, 200

        except exc.SQLAlchemyError as error:
            logging.error(error, exc_info=True)
            return {'message': 'API is down'}, 500
