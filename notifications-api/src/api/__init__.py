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
"""The report Microservice.This module is the API for the Legal Entity system."""

import os

from flask import Flask

import config  # pylint: disable=import-error
from flask import Flask, url_for
from api.resources import API
from flask_oidc import OpenIDConnect
from api.auth.auth import oidc


def create_app(run_mode=os.getenv('FLASK_ENV', 'production')):
    """Return a configured Flask App using the Factory method."""
    app = Flask(__name__)
    app.config.from_object(config.CONFIGURATION[run_mode])  # pylint: disable=no-member
    API.init_app(app)
    oidc.init_app(app)

    @app.after_request
    def add_version(response):  # pylint:  disable=unused-variable
        version = os.getenv('OPENSHIFT_BUILD_COMMIT', '')
        response.headers['API'] = f'notifications_api/{version}'
        return response

    register_shellcontext(app)

    return app


def register_shellcontext(app):
    """Register shell context objects."""

    def shell_context():
        """Shell context objects."""
        return {'app': app}  # pragma: no cover

    app.shell_context_processor(shell_context)
