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
from flask_restx import Resource
from qsystem import application, api
import json
import urllib.request
import urllib.parse
import os
import pysnow
import requests
import json
from app.utilities.auth_util import Role, has_any_role
from app.auth.auth import jwt


@api.route("/feedback/", methods=['POST'])
class Feedback(Resource):

    feedback_destinations = application.config['THEQ_FEEDBACK']
    flag_teams = "TEAMS" in feedback_destinations
    flag_service_now = "SERVICENOW" in feedback_destinations
    flag_rocket_chat = "ROCKETCHAT" in feedback_destinations

    @jwt.has_one_of_roles([Role.internal_user.value])
    def post(self):
        json_data = request.get_json()
        if not json_data:
            return {"message": "Must provide message to send as feedback"}, 400

        try:
            feedback_message = json_data['feedback_message']
        except KeyError:
            return {"message": "Must provide message to send as feedback"}, 422

        teams_result = None
        service_now_result = None
        rocket_chat_result = None

        if self.flag_teams:
            teams_result = Feedback.send_to_teams(feedback_message)

        if self.flag_service_now:
            service_now_result = Feedback.send_to_service_now(feedback_message)

        if self.flag_rocket_chat:
            rocket_chat_result = Feedback.send_to_rocket_chat(feedback_message)

        #  Calculate return message as combination of teams and service now results.
        result = Feedback.combine_results("Teams: ", teams_result, "Service Now: ", service_now_result)
        result = Feedback.combine_results("", result, "Rocket Chat: ", rocket_chat_result)
        return result

    @staticmethod
    def send_to_teams(feedback_message):
        
        url = application.config['TEAMS_URL']

        if url is None:
            return {"message": "TEAMS_URL is not set"}, 400

        feedback_message = feedback_message.replace('\n', '<br />')

        feedback_json_data = {
            "text": feedback_message
        }
        params = json.dumps(feedback_json_data).encode('utf8')
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
        table = application.config['SERVICENOW_TABLE']
        tenant = application.config['SERVICENOW_TENANT']
        assign_group = application.config['SERVICENOW_ASSIGN_GROUP']

        if instance is None:
            return {"message": "SERVICENOW_INSTANCE is not set"}, 400
        if user is None:
            return {"message": "SERVICENOW_USER is not set"}, 400
        if password is None:
            return {"message": "SERVICENOW_PASSWORD is not set"}, 400
        if table is None:
            return {"message": "SERVICENOW_TABLE is not set"}, 400
        if tenant is None:
            return {"message": "SERVICENOW_TENANT is not set"}, 400
        if assign_group is None:
            return {"message": "SERVICENOW_ASSIGN_GROUP is not set"}, 400

        #  Generate Service Now incident.
        #  NOTE:  Automatic email gets sent to the assignment group below
        #         ONLY IF the email of the SERVICENOW_USER IS NOT the same
        #         as the email of this assignment group.

        c = pysnow.Client(instance = instance, user=user, password=password)
        incident = c.resource(api_path=table)
        csr = Feedback.extract_string(params, "Username: ", "\n", 0)
        ticket = Feedback.extract_string(params, "Ticket Number: ","\n", 0)
        msg = Feedback.extract_string(params, "Message: ", "", 50)
        short_desc = "TheQ Feedback (CSR: " + csr + "; Ticket: " + ticket + "; Msg: " + msg + ")"

        #  Create new record depending on tenant value.
        if len(tenant) != 0:
          new_record = {
              'caller_id': user,
              'category': 'Inquiry / Help',
              'cmdb_ci': 'CFMS',
              'u_tenant': tenant,
              'impact': '2 - Some Customers',
              'urgency': '2 - High',
              'priority': 'High',
              'short_description': short_desc,
              'description': params,
              'assignment_group': assign_group
          }
        else:
            new_record = {
                'category': 'Inquiry / Help',
                'cmdb_ci': 'CFMS',
                'impact': '2 - Some Customers',
                'urgency': '2 - High',
                'priority': 'High',
                'short_description': short_desc,
                'description': params,
                'assignment_group': assign_group
            }

        result = incident.create(payload=new_record)

        if '201' in str(result):
            return {"status": "Success"}, 201
        else:
            return {"message": "Service Now incident not created"}, 400

    @staticmethod
    def send_to_rocket_chat(feedback_message):
        
        url = application.config['ROCKET_CHAT_URL']

        if url is None:
            return {"message": "ROCKET_CHAT_URL is not set"}, 400

        feedback_json_data = {
            "text": feedback_message
        }
        params = json.dumps(feedback_json_data).encode('utf8')
        try:
            result = requests.post(url, params)
        except Exception as err:
            return {"message": "Error posting to Rocket Chat. " + str(err)}, 400

        #  See if success or not.
        if result.status_code == 200:
            return {"status": "Success"}, 200
        else:
            return {"message": result.content.decode()}, result.status_code

    @staticmethod
    def extract_string(big_string, key, endstr, max_if_not_found):
        extracted = "Unknown"
        start = big_string.find(key)
        if start >= 0:
            #  End string specified.
            if len(endstr) != 0:
                end = big_string.find(endstr, start+len(key))
            else:
                end = -1

            if end >= 0:
                extracted = big_string[start+len(key):end]
            else:
                if max_if_not_found > 0:
                    extracted = big_string[start+len(key):]
                    extracted = extracted[0:min(max_if_not_found, len(extracted))]

        return extracted

    @staticmethod
    def combine_results(name_one, result_one, name_two, result_two):

        if result_one is None:
            if result_two is None:
                result = {"message": "TheQ is not configured for feedback.  Contact your service desk."}, 400
            else:
                result = result_two

        else:
            if result_two is None:
                result = result_one
            else:
                result = Feedback.extract_messages(name_one, result_one, name_two, result_two)

        return result

    @staticmethod
    def extract_messages(name_one, result_one, name_two, result_two):

        message = ""
        first_result, code = result_one
        second_result, code = result_two

        if 'message' in first_result:
            message = name_one + first_result['message']
        if 'message' in second_result:
            if len(message) != 0:
                message = message + "; " + name_two + second_result['message']
            else:
                message = name_two + second_result['message']

        if message:
            result = {"message": message}, 400
        else:
            result = {"status": "Success"}, 200

        return result
