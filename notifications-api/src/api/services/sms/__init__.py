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
from .sms_base_service import SmsBaseService
import os


def get_sms_service():
    """Return SMS Service implementation."""
    from .custom_notify import CustomNotify
    from .gc_notify import GCNotify

    _instance: SmsBaseService
    if os.getenv('SMS_USE_GC_NOTIFY', 'true').lower() == 'true':
        _instance = GCNotify()
    else:
        _instance = CustomNotify()
    return _instance
