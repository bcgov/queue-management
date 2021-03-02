# Copyright © 2019 Province of British Columbia
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Endpoints to submit citizen feedback."""

from flask import request, jsonify
from flask_restx import Namespace
from flask_restx import Resource, cors
from api.services.feedback import get_feedback_service

api = Namespace('', description='API for submitting feedback')

@api.route('/feedback')
class Feedback(Resource):
    """Feedback resource."""

    def post(self):
        """Submit Feedback."""
        payload = request.get_json(force=True)
        response_code = get_feedback_service().submit(payload)
        print(response_code)
        return jsonify({"response_code":response_code})
