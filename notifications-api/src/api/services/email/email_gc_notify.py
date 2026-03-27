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
"""Send email through GC Notify."""

from flask import current_app
from notifications_python_client import NotificationsAPIClient

from . import EmailBaseService


class EmailGCNotify(EmailBaseService):
    """Implementation for email from GC Notify."""

    def send(self, email_payload):
        """Send email through GC Notify."""
        notifications_client = NotificationsAPIClient(
            api_key=current_app.config["GC_NOTIFY_API_KEY"],
            base_url=current_app.config["GC_NOTIFY_API_BASE_URL"],
        )
        email_to = ",".join(email_payload.get("to", []))
        try:
            response = notifications_client.send_email_notification(
                email_address=email_to,
                template_id=current_app.config["GC_NOTIFY_EMAIL_TEMPLATE_ID"],
                personalisation={
                    "email_subject": email_payload.get("subject"),
                    "email_text": email_payload.get("body"),
                },
            )
            print(response)
        except Exception as exc:  # pragma: no cover
            print(exc)
