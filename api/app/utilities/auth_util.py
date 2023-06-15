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


def get_username() -> str:
    """
    Gets the username in the form user@idp, where username is lowercase
    and the idp is typically one of "bceid", "bcsc", or "idir". Will
    return an empty string if there is no authenticated user identity.
    """
    if 'username' not in g.jwt_oidc_token_info or \
            'identity_provider' not in g.jwt_oidc_token_info:
        return ''

    username = g.jwt_oidc_token_info['username'].lower() + '@' + \
        g.jwt_oidc_token_info['identity_provider']

    return username

def is_public_user() -> bool:
    """Return if the user is a public user or not."""
    return Role.internal_user.value not in g.jwt_oidc_token_info['realm_access'][
        'roles'] and Role.online_appointment_user.value in \
           g.jwt_oidc_token_info['realm_access']['roles']


def has_any_role(roles: list):
    """Check if the user has any role listed in roles."""

    def decorated(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token_roles = g.jwt_oidc_token_info['realm_access']['roles']
            if any(role in token_roles for role in roles):
                return f(*args, **kwargs)
            abort(403)

        return wrapper

    return decorated

def has_role(need_roles: list, all_roles: list, user, caller):
    if any(role in all_roles for role in need_roles):
        return
    else:
        time_print("==> has_role, R: " + str(need_roles) + "; T: " + str(all_roles))
        time_print("    --> U: " + user + "; C:  " + caller)
        abort(403)
