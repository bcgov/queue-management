'''Copyright 2018 Province of British Columbia

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.'''
from enum import Enum
from functools import wraps
from qsystem import time_print

from flask import g, abort


class Role(Enum):
    """Roles."""
    online_appointment_user = 'online_appointment_user'
    internal_user = 'internal_user'
    reminder_job = 'reminder_job'


def is_public_user() -> bool:
    """Return if the user is a public user or not."""
    return Role.internal_user.value not in g.oidc_token_info['realm_access'][
        'roles'] and Role.online_appointment_user.value in \
           g.oidc_token_info['realm_access']['roles']


# def is_job() -> bool:
#     """Return if the user is a reminder job."""
#     return Role.reminder_job.value in g.oidc_token_info['realm_access']['roles']
#

def has_any_role(roles: list):
    """Check if the user has any role listed in roles."""

    def decorated(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token_roles = g.oidc_token_info['realm_access']['roles']
            time_print("==> has_any_role, R: " + str(roles) + "; T: " + str(token_roles))
            time_print("    --> C:  " + str(f))
            if any(role in token_roles for role in roles):
                time_print(f'    --> KW: {kwargs}')
                return f(*args, **kwargs)
            abort(403)

        return wrapper

    return decorated
