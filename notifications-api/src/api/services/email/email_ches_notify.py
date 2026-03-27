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
"""Send email through CHES."""

import json

import requests
from flask import current_app

from . import EmailBaseService


class EmailChesNotify(EmailBaseService):
    """Implementation from Ches Email Notify."""

    def send(self, email_payload):
        """Send email payload through CHES."""
        ches_payload = {
            "bodyType": email_payload.get("bodyType"),
            "body": email_payload.get("body"),
            "from": current_app.config["CHES_EMAIL_FROM_ID"],
            "subject": email_payload.get("subject"),
            "to": email_payload.get("to"),
        }
        try:
            ches_token_response = requests.post(
                current_app.config["CHES_SSO_TOKEN_URL"],
                data=(
                    f"client_id={current_app.config['CHES_SSO_CLIENT_ID']}"
                    f"&client_secret={current_app.config['CHES_SSO_CLIENT_SECRET']}"
                    "&grant_type=client_credentials"
                ),
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                timeout=30,
            )
            ches_api_token = ches_token_response.json().get("access_token")
            email_response = requests.post(
                current_app.config["CHES_POST_EMAIL_ENDPOINT"],
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {ches_api_token}",
                },
                data=json.dumps(ches_payload),
                timeout=30,
            )
            print(email_response)
        except Exception as exc:  # pragma: no cover
            print(exc)
