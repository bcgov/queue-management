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
from app.models.theq import CSR, Office
from flask_restplus import Resource
from app.models.bookings import ExamType
from app.schemas.bookings import ExamSchema
from qsystem import api, api_call_with_retry, db, oidc
from app.utilities.bcmp_service import BCMPService


@api.route("/exams/", methods=["POST"])
class ExamPost(Resource):

    exam_schema = ExamSchema()
    bcmp_service = BCMPService()

    @oidc.accept_token(require_token=True)
    @api_call_with_retry
    def post(self):

        csr = CSR.find_by_username(g.oidc_token_info['username'])

        json_data = request.get_json()

        exam, warning = self.exam_schema.load(json_data)

        if warning:
            logging.warning("WARNING: %s", warning)
            return {"message": warning}, 422

        exam_type = ExamType.query.filter_by(exam_type_id=exam.exam_type_id).first()

        if exam_type.pesticide_exam_ind:
            logging.info("Create BCMP exam since this is a pesticide exam")

            if json_data["sbc_managed"] == "sbc":
                print("Setting sbc_managed shit")
                pesticide_office = Office.query.filter_by(office_name="Pesticide Offsite").first()
                exam.office_id = pesticide_office.office_id

            if exam_type.group_exam_ind:
                logging.info("Creating group pesticide exam")
                bcmp_response = self.bcmp_service.create_group_exam(exam)
            else:
                logging.info("Creating individual pesticide exam")
                bcmp_response = self.bcmp_service.create_group_exam(exam)

            exam.bcmp_job_id = bcmp_response['jobId']
        else:
            if not (exam.office_id == csr.office_id or csr.liaison_designate == 1):
                return {"The Exam Office ID and CSR Office ID do not match!"}, 403

        db.session.add(exam)
        db.session.commit()

        result = self.exam_schema.dump(exam)

        return {"exam": result.data,
                "errors": result.errors}, 201
