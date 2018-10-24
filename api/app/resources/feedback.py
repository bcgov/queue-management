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

from flask import request
from flask_restplus import Resource
from qsystem import application, api, oidc
import json
import urllib.request
import urllib.parse
import os
import pysnow
import requests

@api.route("/feedback/", methods=['POST'])
class Feedback(Resource):

    feedback_destinations = (os.getenv("THEQ_FEEDBACK", "")).upper().replace(" ","").split(",")
    flag_slack = "SLACK" in feedback_destinations
    flag_service_now = "SERVICENOW" in feedback_destinations

    @oidc.accept_token(require_token=True)
    def post(self):
        json_data = request.get_json()
        if not json_data:
            return {"message": "Must provide message to send as feedback"}, 400

        try:
            feedback_message = json_data['feedback_message']
        except KeyError as err:
            return {"message": "Must provide message to send as feedback"}, 422

        if self.flag_slack:
            feedback_json_data = {
                "text": feedback_message
            }
            params = json.dumps(feedback_json_data).encode('utf8')
            slack_result = Feedback.send_to_slack(params)
            print(slack_result)

        if self.flag_service_now:
            service_now_result = Feedback.send_to_service_now(feedback_message)
            print(service_now_result)

        if (not self.flag_slack) and self.flag_service_now:
            return service_now_result

        if (not self.flag_service_now) and self.flag_slack:
            return slack_result

        if self.flag_slack and self.flag_service_now:
            message = ""
            if hasattr(slack_result, 'message'):
                message = slack_result.message
            if hasattr(service_now_result, 'message'):
                if len(message) != 0:
                    message = message + "; " + service_now_result.message
                else:
                    message = service_now_result.message

            if message:
                return {"message": message}, 400
            else:
                return {"status": "Success"}, 200

    @staticmethod
    def send_to_slack(params):

        url = application.config['SLACK_URL']

        if url is None:
            return {"message": "SLACK_URL is not set"}, 400

        req = urllib.request.Request(
            url=url,
            data=params,
            headers={'content-type': 'application/json'}
        )

        resp = urllib.request.urlopen(req)

        if resp.getcode() == 200:
            return {"status": "success"}, 200
        else:
            return {"message": "error", "http_code": resp.getcode()}, 400

    @staticmethod
    def send_to_service_now(params):

        instance = application.config['SERVICENOW_INSTANCE']
        user = application.config['SERVICENOW_USER']
        password = application.config['SERVICENOW_PASSWORD']

        if instance is None:
            return {"message": "SERVICENOW_INSTANCE is not set"}, 400
        if user is None:
            return {"message": "SERVICENOW_USER is not set"}, 400
        if password is None:
            return {"message": "SERVICENOW_PASSWORD is not set"}, 400

        # user = 'CfmsApi'
        # pwd = 'CfmsApi'
        # headers = {"Content-Type": "application/json", "Accept": "application/json"}
        # sndata = '{" short_description": "TheQ created incident" }'
        # response = requests.post(url, auth=(user, pwd), headers=headers, data='{"short_description":"TheQ created incident", "description": "Test incident created by TheQ}')
        # print("Status: ", response.status_code, "Headers: ", response.headers, "Error Response: ", response.json)

        c = pysnow.Client(instance = instance, user=user, password=password)
        incident = c.resource(api_path='/table/incident')
        new_record = {
            #'contact_type': 'Phone',  This isn't working for now. Not critical
            'category': 'Inquiry / Help',
            'cmdb_ci': 'CFMS',
            'impact': '2 - Some Customers',
            'urgency': '2 - High',
            'priority': 'High',
            'short_description': 'TheQ Feedback',
            'description': params,
            'assignment_group': 'Service Delivery Tech Services (GARMS)'
        }

        result = incident.create(payload=new_record)

        if '201' in str(result):
            return {"status": "Success"}, 201
        else:
            return {"message": "Service Now incident not created"}, 400
