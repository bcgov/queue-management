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
"""Flask application factory."""

import os

from flask import Flask

from api import app_config as config
from api.resources import API


def create_app(run_mode: str | None = None):
    """Return a configured Flask application."""
    app = Flask(__name__)
    app.config.from_object(config.get_named_config(run_mode))
    API.init_app(app)
    setup_jwt_manager(app)

    @app.after_request
    def add_version(response):
        version = os.getenv("OPENSHIFT_BUILD_COMMIT", "")
        response.headers["API"] = f"notifications_api/{version}"
        return response

    register_shellcontext(app)
    return app


def setup_jwt_manager(app):
    """Configure the JWT manager for the app."""
    from api.auth.auth import jwt as jwt_manager

    def get_roles(a_dict):
        return a_dict["realm_access"]["roles"]  # pragma: no cover

    app.config["JWT_ROLE_CALLBACK"] = get_roles
    jwt_manager.init_app(app)


def register_shellcontext(app):
    """Register shell context objects."""

    def shell_context():
        return {"app": app}  # pragma: no cover

    app.shell_context_processor(shell_context)
