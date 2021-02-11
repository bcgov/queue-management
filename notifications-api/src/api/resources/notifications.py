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

from api.auth.auth import oidc
from api.services.sms import get_sms_service

api = Namespace('notifications', description='API for Sending Service BC Notifications')


@api.route('/sms')
class SmsNotification(Resource):
    """Notification resource."""

    @oidc.accept_token(require_token=True)
    def post(self):
        """Send notification."""
        sms_payload = request.get_json(force=True)
        get_sms_service().send(sms_payload)
        return jsonify({})
