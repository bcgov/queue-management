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
"""Provides the WSGI entry point for running the application."""

from api import create_app

application = create_app()


def _config_flag(name, default=False):
    value = application.config.get(name)
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "on"}


if __name__ == "__main__":
    application.run(
        host=application.config.get("WSGI_HOST", "0.0.0.0"),
        port=int(application.config.get("WSGI_PORT", 5002)),
        debug=_config_flag("WSGI_DEBUG", True),
        use_reloader=_config_flag("WSGI_USE_RELOADER", False),
    )
