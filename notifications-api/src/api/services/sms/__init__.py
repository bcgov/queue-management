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
"""SMS provider selection."""

from flask import current_app

from .sms_base_service import SmsBaseService


def get_sms_provider() -> str:
    """Return the normalized SMS provider."""
    provider = current_app.config.get("SMS_PROVIDER", "")
    normalized = provider.strip().upper() if isinstance(provider, str) else ""
    return normalized or "CUSTOM"


def get_sms_service():
    """Return SMS service implementation."""
    from .custom_notify import CustomNotify
    from .gc_notify import GCNotify
    from .log_notify import SmsLogNotify

    provider = get_sms_provider()
    current_app.config["SMS_PROVIDER"] = provider
    current_app.config["SMS_USE_GC_NOTIFY"] = provider == "GC_NOTIFY"

    instance: SmsBaseService
    if provider == "GC_NOTIFY":
        instance = GCNotify()
    elif provider == "LOG":
        instance = SmsLogNotify()
    else:
        instance = CustomNotify()
    return instance
