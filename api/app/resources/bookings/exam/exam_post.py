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
import copy
import json
from flask import request, g
from flask_restx import Resource
from app.models.theq import CSR, Office
from flask_restplus import Resource
from app.models.bookings import ExamType, Invigilator
from app.schemas.bookings import ExamSchema, CandidateSchema
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

        print("json_data: ")
        print(json_data)

        if warning:
            logging.warning("WARNING: %s", warning)
            return {"message": warning}, 422
        print("+=+=+=+= NAME: %s +=+=+=+=" % exam.examinee_name)

        exam_type = ExamType.query.filter_by(exam_type_id=exam.exam_type_id).first()

        if not exam_type:
            exam_type = ExamType.query.filter_by(pesticide_exam_ind=1, group_exam_ind=1).first()
            exam.exam_type = exam_type

        invigilator = None
        if exam.invigilator_id:
            invigilator = Invigilator.query.filter_by(invigilator_id=exam.invigilator_id).first()

        if json_data["sbc_managed"] != "sbc":
            pesticide_office = Office.query.filter_by(office_name="Pesticide Offsite").first()
            exam.office_id = pesticide_office.office_id

        if (json_data["ind_or_group"] == "individual"):
            if exam_type.pesticide_exam_ind:
                
                exam_fees = json_data["fees"]
                
                logging.info("Creating individual pesticide exam")
                bcmp_response = self.bcmp_service.create_individual_exam(exam, exam_type, exam_fees, invigilator)

                if bcmp_response:
                    exam.bcmp_job_id = bcmp_response['jobId']
            else:
                if not (exam.office_id == csr.office_id or csr.liaison_designate == 1):
                    return {"The Exam Office ID and CSR Office ID do not match!"}, 403
        else:
            logging.info("For Group Exams")
            print(json_data["candidates"])

            if json_data["candidates"]:
                candidates = json_data["candidates"]
                candidates_list = []
                candidates_list_bcmp = []
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
                    print(candidate["exam_type_id"])
                    candidates_bcmp = copy.deepcopy(candidate_temp)
                    exam_type = ExamType.query.filter_by(exam_type_id=candidate["exam_type_id"]).first()
                    if exam_type.exam_type_name:
                        candidates_bcmp["exam_type"] = exam_type.exam_type_name
                        print(candidates_bcmp["exam_type"])
                    candidates_list_bcmp.append(candidates_bcmp)

                print("candidates_list")
                print(candidates_list)
                print("saving to exam obj")
                
                exam.candidates_list = candidates_list

                pesticide_office = Office.query.filter_by(office_id=exam.office_id).first()

                logging.info("Creating Group pesticide exam")
                bcmp_response = self.bcmp_service.create_group_exam_bcmp(exam, candidates_list_bcmp, invigilator, pesticide_office)

                if bcmp_response:
                    exam.bcmp_job_id = bcmp_response['jobId']
                    

        db.session.add(exam)
        db.session.commit()

        result = self.exam_schema.dump(exam)

        return {"exam": result.data,
                "errors": result.errors}, 201
