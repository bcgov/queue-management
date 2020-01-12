import json
import urllib
from qsystem import application
from app.utilities.document_service import DocumentService


class BCMPService:
    base_url = application.config['BCMP_BASE_URL']
    auth_token = application.config['BCMP_AUTH_TOKEN']

    def __init__(self):
        return

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

        print('response')
        print(response.status)

        return json.loads(response.read().decode('utf-8'))

    def check_exam_status(self, exam):
        url = "%s/auth=env_exam;%s/JSON/status" % (self.base_url, self.auth_token)
        data = {
            "jobs": [
                exam.bcmp_job_id
            ]
        }
        response = self.send_request(url, 'POST', data)
        print(response)

        for job in response['jobs']:
            print(job)
            if job['jobId'] == exam.bcmp_job_id:
                return job['jobStatus']

        return response

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

    def create_individual_exam(self, exam, exam_type):
        url = "%s/auth=env_exam;%s/JSON/create:ENV-IPM-EXAM" % (self.base_url, self.auth_token)
        bcmp_exam = {
            "category": exam_type.exam_type_name,
            "students": [
                {"name": exam.examinee_name}
            ]
        }

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

        self.send_request(url, "POST", json_data)
