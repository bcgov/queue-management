import json
import logging
import urllib
from qsystem import application, my_print
from app.utilities.document_service import DocumentService
from datetime import datetime
import pytz
from dateutil import parser

class BCMPService:
    base_url = application.config['BCMP_BASE_URL']
    auth_token = application.config['BCMP_AUTH_TOKEN']
    bcmp_user = application.config["BCMP_USER"]

    def __init__(self):
        return
    
    def __exam_time_format(self, date_value):
        return date_value.strftime("%a %b %d, %Y at %-I:%M %p")

    def send_request(self, path, method, data):
        if method == 'POST':
            request_data = bytes(json.dumps(data), encoding="utf-8")
        else:
            request_data = None

        my_print("=== SENDING BCMP REQUEST ===")
        my_print("  ==> url: %s" % path)
        my_print("  ==> method: %s" % method)
        my_print("  ==> data: %s" % request_data)
        req = urllib.request.Request(path, data=request_data, method=method)
        req.add_header('Content-Type', 'application/json')
        my_print('request')
        my_print(req)

        response = urllib.request.urlopen(req)
        

        response_data = response.read().decode('utf8')
        my_print(response_data)
        logging.warning("Response data: %s" % response_data)

        try:
            return json.loads(response_data)
        except json.decoder.JSONDecodeError:
            logging.warning("Error decoding JSON response data. Response data: %s" % response_data)
            return False

    def check_exam_status(self, exam):
        url = "%s/auth=%s;%s/JSON/status" % (self.base_url, self.bcmp_user, self.auth_token)
        my_print("  ==> check_exam_status   url: %s" % url)
        data = {
            "jobs": [
                exam.bcmp_job_id
            ]
        }
        response = self.send_request(url, 'POST', data)

        if response and response['jobs']:
            for job in response['jobs']:
                my_print(job)
                if job['jobId'] == exam.bcmp_job_id:
                    return job

        return False

    def bulk_check_exam_status(self, exams):
        url = "%s/auth=%s;%s/JSON/status" % (self.base_url, self.bcmp_user, self.auth_token)
        my_print("  ==> bulk_check_exam_status    url: %s" % url)
        data = {
            "jobs": []
        }

        for exam in exams:
            data["jobs"].append(exam.bcmp_job_id)

        response = self.send_request(url, 'POST', data)
        my_print(response)

        return response

    def create_individual_exam(self, exam, exam_fees, invigilator, pesticide_office, oidc_token_info):
        my_print("  ==> create_individual_exam self base_url: %s" % self.base_url)
        my_print("  ==> create_individual_exam self bcmp_user: %s" % self.bcmp_user)
        my_print("  ==> create_individual_exam self auth_token: %s" % self.auth_token)
        url = "%s/auth=%s;%s/JSON/create:BCMD-EXAM" % (self.base_url, self.bcmp_user, self.auth_token)
        my_print("  ==> create_individual_exam  url: %s" % url)

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
            "REGISTRAR_name" : oidc_token_info['username'],
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

    def create_group_exam_bcmp(self, exam, booking, candiate_list, pesticide_office, oidc_token_info):
        url = "%s/auth=%s;%s/JSON/create:BCMD-EXAM-GROUP" % (self.base_url, self.bcmp_user, self.auth_token)
        my_print("  ==> create_group_exam_bcmp    url: %s" % url)

        office_name = None
        time_zone = pytz.timezone('America/Vancouver')
        if pesticide_office:
            office_name = pesticide_office.office_name
            time_zone = pytz.timezone(pesticide_office.timezone.timezone_name)

        my_print(exam.expiry_date.strftime("%a %b %d, %Y at %-I:%M %p"))
        exam_text = None
        if booking:
            exam_utc = parser.parse(booking["start_time"])
            exam_time = exam_utc.astimezone(tz=time_zone)
            exam_text = self.__exam_time_format(exam_time)

        bcmp_exam = {
            "EXAM_SESSION_LOCATION": office_name,
            "REGISTRAR_name" : oidc_token_info['username'],
            "RECIPIENT_EMAIL_ADDRESS" : oidc_token_info['email'],
            "REGISTRAR_phoneNumber": "",
            "students": []
        }

        if exam_text:
            bcmp_exam["SESSION_DATE_TIME"] = exam_text

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
        url = "%s/auth=%s;%s/JSON/create:BCMD-EXAM" % (self.base_url, self.bcmp_user, self.auth_token)
        my_print("  ==> create_group_exam    url: %s" % url)

        bcmp_exam = {
            "students": []
        }

        for s in exam.students:
            bcmp_exam["students"].append({"name": s.name})

        response = self.send_request(url, 'POST', bcmp_exam)
        return response

    def send_exam_to_bcmp(self, exam):
        url = "%s/auth=%s;%s/JSON/create:BCMD-EXAM-API-ACTION" % (self.base_url, self.bcmp_user, self.auth_token)
        my_print("  ==> send_exam_to_bcmp    url: %s" % url)

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
        url = "%s/auth=%s;%s/JSON/create:BCMD-EXAM-API-ACTION" % (self.base_url, self.bcmp_user, self.auth_token)
        my_print("  ==> email_exam_invigilator    url: %s" % url)

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
