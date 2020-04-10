import json
import logging
import urllib
from qsystem import application
from app.utilities.document_service import DocumentService
from datetime import datetime


class BCMPService:
    base_url = application.config['BCMP_BASE_URL']
    auth_token = application.config['BCMP_AUTH_TOKEN']

    def __init__(self):
        return
    
    def __exam_time_format(self, date_value):
        return date_value.strftime("%a %b %d, %Y at %-I:%M %p")

    def send_request(self, path, method, data):
        if method == 'POST':
            request_data = bytes(json.dumps(data), encoding="utf-8")
        else:
            request_data = None

        print("=== SENDING BCMP REQUEST ===")
        print("  ==> url: %s" % path)
        print("  ==> method: %s" % method)
        print("  ==> data: %s" % request_data)
        req = urllib.request.Request(path, data=request_data, method=method)
        req.add_header('Content-Type', 'application/json')
        print('request')
        print(req)

        response = urllib.request.urlopen(req)
        

        response_data = response.read().decode('utf8')
        print(response_data)

        try:
            return json.loads(response_data)
        except json.decoder.JSONDecodeError:
            logging.warning("Error decoding JSON response data. Response data: %s" % response_data)
            return False

    def check_exam_status(self, exam):
        url = "%s/auth=env_exam;%s/JSON/status" % (self.base_url, self.auth_token)
        data = {
            "jobs": [
                exam.bcmp_job_id
            ]
        }
        response = self.send_request(url, 'POST', data)

        if response and response['jobs']:
            for job in response['jobs']:
                print(job)
                if job['jobId'] == exam.bcmp_job_id:
                    return job

        return False

    def bulk_check_exam_status(self, exams):
        url = "%s/auth=env_exam;%s/JSON/status" % (self.base_url, self.auth_token)
        data = {
            "jobs": []
        }

        for exam in exams:
            data["jobs"].append(exam.bcmp_job_id)

        response = self.send_request(url, 'POST', data)
        print(response)

        return response

    def create_individual_exam(self, exam, exam_fees, invigilator, pesticide_office, oidc_token_info):
        url = "%s/auth=env_exam;%s/JSON/create:ENV-IPM-EXAM" % (self.base_url, self.auth_token)

        office_name = None
        if pesticide_office:
            office_name = pesticide_office.office_name

        receipt_number = "%s fees" % exam_fees
        if exam.receipt:
            receipt_number = exam.receipt
        
        exam_type_name = None
        if exam.exam_type:
            exam_type_name = exam.exam_type.exam_type_name

        invigilator_name = None
        if invigilator:
            invigilator_name = invigilator.invigilator_name

        bcmp_exam = {
            "EXAM_SESSION_LOCATION" : office_name,
            "SESSION_DATE_TIME" : self.__exam_time_format(exam.expiry_date),
            "REGISTRAR_name" : oidc_token_info['preferred_username'],
            "RECIPIENT_EMAIL_ADDRESS" : oidc_token_info['email'],
            "REGISTRAR_phoneNumber" : "",
            "students": [
                {
                    "REGISTRAR_name": invigilator_name,
                    "EXAM_CATEGORY": exam_type_name,
                    "STUDENT_LEGAL_NAME_first": exam.examinee_name,
                    "STUDENT_LEGAL_NAME_last": exam.examinee_name,
                    "STUDENT_emailAddress": exam.examinee_email,
                    "STUDENT_phoneNumber": exam.examinee_phone,
                    "REGISTRATION_NOTES": exam.notes,
                    "RECEIPT_RMS_NUMBER": receipt_number
                }
            ]
        }

        response = self.send_request(url, 'POST', bcmp_exam)
        return response

    def create_group_exam_bcmp(self, exam, candiate_list, invigilator, pesticide_office, oidc_token_info):
        url = "%s/auth=env_exam;%s/JSON/create:ENV-IPM-EXAM-GROUP" % (self.base_url, self.auth_token)

        invigilator_name = None
        if invigilator:
            invigilator_name = invigilator.invigilator_name

        office_name = None
        if pesticide_office:
            office_name = pesticide_office.office_name

        print(exam.expiry_date.strftime("%a %b %d, %Y at %-I:%M %p"))
        
        bcmp_exam = {
            "EXAM_SESSION_LOCATION": office_name,
            "SESSION_DATE_TIME" : self.__exam_time_format(exam.expiry_date),
            "REGISTRAR_name" : oidc_token_info['preferred_username'],
            "RECIPIENT_EMAIL_ADDRESS" : oidc_token_info['email'],
            "REGISTRAR_phoneNumber": "",
            "students": []
        }

        for candiate in candiate_list:
            bcmp_exam["students"].append({
                "EXAM_CATEGORY": candiate["exam_type"],
                "STUDENT_LEGAL_NAME_first": candiate["examinee_name"],
                "STUDENT_LEGAL_NAME_last": candiate["examinee_name"],
                "STUDENT_emailAddress": candiate["examinee_email"],
                "STUDENT_phoneNumber": "",
                "STUDENT_ADDRESS_line1": "",
                "STUDENT_ADDRESS_line2": "",
                "STUDENT_ADDRESS_city": "",
                "STUDENT_ADDRESS_province": "",
                "STUDENT_ADDRESS_postalCode": "",
                "REGISTRATION_NOTES": "",
                "RECEIPT_RMS_NUMBER": candiate["receipt"],
                "PAYMENT_METHOD": candiate["fees"],
                "FEE_PAYMENT_NOTES": ""
            })

        response = self.send_request(url, 'POST', bcmp_exam)
        return response

    def create_group_exam(self, exam):
        url = "%s/auth=env_exam;%s/JSON/create:ENV-IPM-EXAM" % (self.base_url, self.auth_token)

        bcmp_exam = {
            "students": []
        }

        for s in exam.students:
            bcmp_exam["students"].append({"name": s.name})

        response = self.send_request(url, 'POST', bcmp_exam)
        return response

    def send_exam_to_bcmp(self, exam):
        url = "%s/auth=env_exam;%s/JSON/create:ENV-IPM-EXAM-API-ACTION" % (self.base_url, self.auth_token)

        client = DocumentService(
            application.config["MINIO_HOST"],
            application.config["MINIO_BUCKET"],
            application.config["MINIO_ACCESS_KEY"],
            application.config["MINIO_SECRET_KEY"],
            application.config["MINIO_USE_SECURE"]
        )

        filename = "%s.pdf" % exam.exam_id

        presigned_url = client.get_presigned_get_url(filename)
        json_data = {
            "action": {
                "jobId": exam.bcmp_job_id,
                "actionName": "UPLOAD_RESPONSE_PDF",
                "remoteUrl": presigned_url
            }
        }

        response = self.send_request(url, 'POST', json_data)
        return response

    def email_exam_invigilator(self, exam, invigilator_name, invigilator_email, invigilator_phone):
        url = "%s/auth=env_exam;%s/JSON/create:ENV-IPM-EXAM-API-ACTION" % (self.base_url, self.auth_token)

        json_data = {
            "action": {
                "jobId": exam.bcmp_job_id,
                "actionName": "SEND_TO_INVIGILATOR",
                "invigilatorName": invigilator_name,
                "invigilatorEmailAddress": invigilator_email,
                "invigilatorPhoneNumber": invigilator_phone
            }
        }

        response = self.send_request(url, "POST", json_data)

        return response
