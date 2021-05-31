# Copyright © 2019 Province of British Columbia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Submit Citizen feedback.

This module consists of API that calls Camunda BPM to save citizen feedback comments.
"""
import os, requests, json
from typing import Dict
from jinja2 import Environment, FileSystemLoader
from .feedback_base_service import FeedbackBaseService
from flask import jsonify


class FeedbackCamundaService(FeedbackBaseService):
    """Implementation from FeedbackService."""

    def submit(self, payload):
        """Submit feedback to Camunda API"""
        camunda_service_endpoint = os.getenv('FEEDBACK_CAMUNDA_URL')
        keycloak_endpoint = os.getenv('FEEDBACK_AUTH_URL')
        keycloak_client_id = os.getenv('FEEDBACK_AUTH_CLIENT_ID')
        keycloak_client_secret = os.getenv('FEEDBACK_AUTH_CLIENT_SECRET')
        
        auth_payload = {"grant_type":"client_credentials",
                "client_id":keycloak_client_id,
                "client_secret":keycloak_client_secret}
        try:
            auth_response = requests.post(keycloak_endpoint,data=auth_payload)
            access_token = auth_response.json()['access_token']
            headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {access_token}'}
            feedback_response = requests.post(camunda_service_endpoint,
                                headers=headers,
                                data=json.dumps(payload), timeout=10.0)
            response_code = feedback_response.status_code
            if (response_code != 200 and response_code != 201 and response_code != 202) :
                raise Exception('Camunda API Failure')
            return feedback_response.status_code
        except Exception as e:
            feedback_type = payload['variables']['engagement']['value']
            feedback_message = payload['variables']['citizen_comments']['value']
            response_required = payload['variables']['response']['value']
            citizen_name = payload['variables']['citizen_name']['value']
            citizen_contact = payload['variables']['citizen_contact']['value']
            citizen_email = payload['variables']['citizen_email']['value']
            service_date = payload['variables']['service_date']['value']
            submit_date_time = payload['variables']['submit_date_time']['value']

            ENV = Environment(loader=FileSystemLoader('.'), autoescape=True)
            template = ENV.get_template('camunda_email_template.template')
            body = template.render(feedback_type =feedback_type,
                           feedback_message =feedback_message,
                           response_required =response_required,
                           citizen_name =citizen_name,
                           citizen_contact =citizen_contact,
                           citizen_email =citizen_email,
                           service_date =service_date,
                           submit_date_time =submit_date_time)

            application_auth_url = os.getenv('APP_AUTH_URL')
            application_client_id = os.getenv('APP_AUTH_CLIENT_ID')
            application_client_secret = os.getenv('APP_AUTH_CLIENT_SECRET')
            notification_email_url = os.getenv('NOTIFICATION_EMAIL_URL')
            email_to = (os.getenv('NOTIFICATION_EMAIL_TO')).split(",")
            app_auth_payload = {"grant_type":"client_credentials",
                "client_id":application_client_id,
                "client_secret":application_client_secret}
            email_payload = {
                'bodyType': 'text',
                'body': body,
                'subject': 'Citizen Feedback - Camunda API failure',
                'to': email_to
            }
            app_auth_response = requests.post(application_auth_url,data=app_auth_payload)
            app_access_token = app_auth_response.json()['access_token']
            email_headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {app_access_token}'}
            email_response = requests.post(notification_email_url,
                                headers=email_headers,
                                data=json.dumps(email_payload))
            print(email_response)
            print(e)
            return email_response.status_code
        
