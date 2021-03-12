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
from .email_base_service import EmailBaseService
import os


def get_email_service():
    """Return SMS Service implementation."""
    from .email_gc_notify import EmailGCNotify
    from .email_ches_notify import EmailChesNotify

    _instance: EmailBaseService = None
    if os.getenv('EMAIL_USE_GC_NOTIFY', 'false').lower() == 'true':
        _instance = EmailGCNotify()
    else:
        _instance = EmailChesNotify()
    return _instance
