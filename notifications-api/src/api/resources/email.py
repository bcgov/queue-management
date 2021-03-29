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
"""Endpoints to check manage notifications."""

from flask import request, jsonify
from flask_restx import Namespace
from flask_restx import Resource

from api.auth.auth import jwt
from api.services.email import get_email_service

api = Namespace('notifications', description='API for Sending Service BC Notifications')


@api.route('/email')
class EmailNotification(Resource):
    """Notification resource."""
    @jwt.requires_auth
    def post(self):
        """Send email notification."""
        email_payload = request.get_json(force=True)
        get_email_service().send(email_payload)
        return jsonify({})
