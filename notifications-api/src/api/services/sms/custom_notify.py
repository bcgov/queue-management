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
"""Send SMS reminder.

This module is being invoked from a job and it sends SMS reminders to customers.
"""
import os
from typing import Dict

from . import SmsBaseService


class CustomNotify(SmsBaseService):
    """Implementation from BC Notify."""

    def send(self, appointments: Dict):
        """Send SMS reminders for next day appointments."""
        print('<---- Inside Custom Notify ---->')
        return None
