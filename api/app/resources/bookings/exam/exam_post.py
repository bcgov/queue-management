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

import copy

import logging
from flask import request
from flask_restx import Resource

from app.auth.auth import jwt
from app.models.bookings import ExamType
from app.models.theq import CSR, Office
from app.schemas.bookings import ExamSchema
from app.utilities.auth_util import Role, get_username
from app.utilities.bcmp_service import BCMPService
from qsystem import api, api_call_with_retry, db, my_print


@api.route("/exams/", methods=["POST"])
class ExamPost(Resource):

    exam_schema = ExamSchema()
    bcmp_service = BCMPService()

    @jwt.has_one_of_roles([Role.internal_user.value])
    @api_call_with_retry
    def post(self):

        is_bcmp_req = True if request.args.get('bcmp_pesticide') else False

        my_print("is_bcmp_req: ")
        my_print(is_bcmp_req)

        csr = CSR.find_by_username(get_username())

        json_data = request.get_json()

        exam = self.exam_schema.load(json_data)
        warning = self.exam_schema.validate(json_data)

        my_print("json_data: ")
        my_print(json_data)

        if warning:
            logging.warning("WARNING: %s", warning)
            return {"message": warning}, 422
        
        if not (exam.office_id == csr.office_id or csr.ita2_designate == 1):
            return {"The Exam Office ID and CSR Office ID do not match!"}, 403   
        
        if exam.is_pesticide:
            formatted_data = self.format_data(json_data, exam)
            exam = formatted_data["exam"]
            job = self.bcmp_service.check_exam_status(exam)
            my_print(job)
            #if job and job['jobProperties'] and job['jobProperties']['JOB_ID']:
                #exam.event_id = job['jobProperties']['JOB_ID']

        db.session.add(exam)
        db.session.commit()

        result = self.exam_schema.dump(exam)

        return {"exam": result,
                "errors": self.exam_schema.validate(exam)}, 201



    ## formating data to save on bcmp
    def format_data(self, json_data, exam):

        candidates_list_bcmp = []

        pesticide_office = None
        if json_data["sbc_managed"] == "sbc":
            pesticide_office = Office.query.filter_by(office_id=exam.office_id).first()
        else:
            pesticide_office = Office.query.filter_by(office_name="Pesticide Offsite").first()
            exam.office_id = pesticide_office.office_id

        if json_data["ind_or_group"] == "individual":
        
            exam_type = ExamType.query.filter_by(exam_type_id=exam.exam_type_id).first()

            if not exam_type:
                exam_type = ExamType.query.filter_by(pesticide_exam_ind=1, group_exam_ind=1).first()
            exam.exam_type = exam_type

        else:
            logging.info("For Group Exams")

            exam_type = ExamType.query.filter_by(exam_type_name="Group Environment Exam").first()
            if exam_type:
                exam.exam_type_id = exam_type.exam_type_id
                exam.exam_type = exam_type

            if json_data["candidates"]:
                candidates = json_data["candidates"]
                candidates_list = []
                for candidate in candidates:
                    candidate_temp = {}
                    candidate_temp["examinee_name"] = candidate["name"]
                    candidate_temp["examinee_email"] = candidate["email"]
                    candidate_temp["exam_type_id"] = candidate["exam_type_id"]
                    candidate_temp["fees"] = candidate["fees"]
                    candidate_temp["payee_ind"] = 1 if (candidate["billTo"] == "candidate") else 0
                    candidate_temp["receipt"] = candidate["receipt"]
                    candidate_temp["receipt_number"] = candidate["receipt"]
                    candidate_temp["payee_name"] = candidate["payeeName"]
                    candidate_temp["payee_email"] = candidate["payeeEmail"]
                    candidates_list.append(candidate_temp)
                    # for bcmp service
                    candidates_bcmp = copy.deepcopy(candidate_temp)
                    exam_type = ExamType.query.filter_by(exam_type_id=candidate["exam_type_id"]).first()
                    if exam_type.exam_type_name:
                        candidates_bcmp["exam_type"] = exam_type.exam_type_name
                    candidates_list_bcmp.append(candidates_bcmp)

                exam.candidates_list = candidates_list
        
        return { 
            'exam': exam, 
            'candidates_list_bcmp': candidates_list_bcmp, 
            'pesticide_office': pesticide_office,
        }

