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


@api.route("/slack/", methods=['POST'])
class Slack(Resource):

    @oidc.accept_token(require_token=True)
    def post(self):
        json_data = request.get_json()
        if not json_data:
            return {"message": "Must provide message to send to slack"}, 400

        try:
            slack_message = json_data['slack_message']
        except KeyError as err:
            return {"message": "Must provide message to send to slack"}, 422

        slack_json_data = {
            "text": slack_message
        }

        print(slack_json_data)
        params = json.dumps(slack_json_data).encode('utf8')

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
            return {"status": "error", "http_code": resp.getcode()}, 400

        return {"message": "Success"}, 200
