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

from app.auth.auth import jwt
from app.models.bookings import Invigilator
from app.models.theq import CSR
from app.resources.bookings.exam.exam_post import ExamPost
from app.schemas.bookings import ExamSchema
from app.utilities.auth_util import get_username
from app.utilities.bcmp_service import BCMPService
from qsystem import api, api_call_with_retry


@api.route("/exams/bcmp/", methods=["POST"])
class ExamBcmpPost(Resource):

    exam_schema = ExamSchema()
    bcmp_service = BCMPService()

    @jwt.requires_auth
    @api_call_with_retry
    def post(self):

        csr = CSR.find_by_username(get_username())

        json_data = request.get_json()

        if 'bookdata' in json_data.keys():
            booking = json_data["bookdata"]
        else:
            booking = None

        exam = self.exam_schema.load(json_data)
        warning = self.exam_schema.validate(json_data)

        if warning:
            logging.warning("WARNING: %s", warning)
            return {"message": warning}, 422
        
        if not (exam.office_id == csr.office_id or csr.ita2_designate == 1):
            return {"The Exam Office ID and CSR Office ID do not match!"}, 403   
            
        formatted_data = ExamPost.format_data(self, json_data, exam)
        exam = formatted_data["exam"]

        invigilator = None
        if exam.invigilator_id:
            invigilator = Invigilator.query.filter_by(invigilator_id=exam.invigilator_id).first()

        bcmp_response = None
        if json_data["ind_or_group"] == "individual":
            
            exam_fees = json_data["fees"]
            
            logging.info("Creating individual pesticide exam")
            bcmp_response = self.bcmp_service.create_individual_exam(exam, exam_fees, invigilator, formatted_data["pesticide_office"], g.jwt_oidc_token_info)

        else:

            logging.info("Creating Group Environment exam")
            bcmp_response = self.bcmp_service.create_group_exam_bcmp(exam, booking, formatted_data["candidates_list_bcmp"], formatted_data["pesticide_office"], g.jwt_oidc_token_info)
            
            
        if bcmp_response:
            return {"bcmp_job_id": bcmp_response['jobId'],
                "errors": {}}, 201
        else:
            return {"message": "create_group_exam_bcmp failed",
                "error": bcmp_response}, 403

