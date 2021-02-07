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
"""Meta information about the service.

Currently this only provides API versioning information
"""
from flask import jsonify
from flask_restx import cors
from flask_restx import Resource
from flask_restx import Namespace
import os

api = Namespace('', description='API for Sending Service BC Notifications')


@api.route('/info')
class Info(Resource):
    """Meta information about the overall service."""

    @cors.crossdomain(origin='*')
    def get(self):
        """Return a JSON object with meta information about the Service."""
        version = os.getenv('OPENSHIFT_BUILD_COMMIT', '')
        return jsonify(API=f'notifications_api/{version}')
