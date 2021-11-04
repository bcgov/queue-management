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

from flask import request, jsonify, g
from flask_restx import Resource
import sqlalchemy.orm
from qsystem import application, api, db, socketio
from app.auth import required_scope
from app.models.theq import Citizen, CSR
from cockroachdb.sqlalchemy import run_transaction
import logging
from marshmallow import ValidationError, pre_load
from sqlalchemy import exc
import json
import urllib.request
import urllib.parse
from app.utilities.auth_util import Role, has_any_role
from app.auth.auth import jwt


@api.route("/slack/", methods=['POST'])
class Slack(Resource):

    @jwt.has_one_of_roles([Role.internal_user.value])
    def post(self):
        json_data = request.get_json()
        if not json_data:
            return {"message": "Must provide message to send to slack"}, 400

        try:
            slack_message = json_data['slack_message']
        except KeyError:
            return {"message": "Must provide message to send to slack"}, 422

        print(slack_message)

        slack_json_data = {
            "text": slack_message
        }

        print(slack_json_data)
        params = json.dumps(slack_json_data).encode('utf8')

        req = urllib.request.Request(
            url=application.config['SLACK_URL'], 
            data=params,
            headers={'content-type': 'application/json'}
        )

        resp = urllib.request.urlopen(req)

        print(req)
        print(resp)
