import json
import logging
import urllib
from qsystem import application


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

        req = urllib.request.Request(path, data=request_data, method=method)
        req.add_header('Content-Type', 'application/json')
        print('request')
        print(req)

        response = urllib.request.urlopen(req).read()

        print('response')
        print(response)

        return json.loads(response.decode('utf-8'))

    def check_exam_status(self, exam):
        url = "%s/auth=env_exam;%s/JSON/create:ENV-IPM-EXAM" % (self.base_url, self.auth_token)
        data = {
            "jobs": [
                exam.bcmp_job_id
            ]
        }
        response = self.send_request(url, 'POST', data)

        return response

    def create_individual_exam(self, exam):
        url = "%s/auth=env_exam;%s/JSON/create:ENV-IPM-EXAM" % (self.base_url, self.auth_token)
        bcmp_exam = {
            "name": "",
            "email": ""
        }

        response = self.send_request(url, 'POST', bcmp_exam)
        return response

    def create_group_exam(self, exam):
        url = "%s/auth=env_exam;%s/JSON/create:ENV-IPM-EXAM" % (self.base_url, self.auth_token)

        bcmp_exam = {
            "students": [{
                "name": "",
                "email": ""
            }]
        }

        response = self.send_request(url, 'POST', bcmp_exam)
        return response
