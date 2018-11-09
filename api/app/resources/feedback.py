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
import json

@api.route("/feedback/", methods=['POST'])
class Feedback(Resource):

    feedback_destinations = application.config['THEQ_FEEDBACK']
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

        slack_result = None
        service_now_result = None

        if self.flag_slack:
            feedback_json_data = {
                "text": feedback_message
            }
            params = json.dumps(feedback_json_data).encode('utf8')
            slack_result = Feedback.send_to_slack(params)

        if self.flag_service_now:
            service_now_result = Feedback.send_to_service_now(feedback_message)

        #  Calculate return message as combination of slack and service now results.
        result = Feedback.combine_results(slack_result, service_now_result)
        return result

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
            return {"status": "Success"}, 200
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

    @staticmethod
    def combine_results(slack_result, service_now_result):

        if slack_result is None:
            if service_now_result is None:
                print("    --> slack none, service now none")
                result = {"message": "TheQ is not configured for feedback.  Contact your service desk."}, 400
            else:
                print("    --> slack none, service now result")
                result = service_now_result

        else:
            if service_now_result is None:
                print("    --> slack result, service now none")
                result = slack_result
            else:
                print("    --> slack result, service now result")
                result = Feedback.extract_messages(slack_result, service_now_result)

        return result

    @staticmethod
    def extract_messages(slack, service_now):

        message = ""
        slack_result, code = slack
        service_now_result, code = service_now

        if 'message' in slack_result:
            message = slack_result['message']
        if 'message' in service_now_result:
            if len(message) != 0:
                message = message + "; " + service_now_result['message']
            else:
                message = service_now_result['message']

        if message:
            result = {"message": message}, 400
        else:
            result = {"status": "Success"}, 200

        return result
