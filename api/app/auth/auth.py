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
"""Auth."""
from typing import Dict

from flask_jwt_oidc import JwtManager
from flask_jwt_oidc.exceptions import AuthError
from jose import jwt as jwt_parser

jwt = JwtManager()


def decode_token(token: str) -> Dict:
    """Validate the token"""
    try:
        unverified_header = jwt_parser.get_unverified_header(token)
    except jwt_parser.JWTError as jerr:
        raise AuthError({'code': 'invalid_header',
                         'description':
                             'Invalid header. '
                             'Use an RS256 signed JWT Access Token'}, 401) from jerr

    rsa_key = jwt.get_rsa_key(jwt.get_jwks(), unverified_header['kid'])

    if not rsa_key:
        raise AuthError({'code': 'invalid_header',
                         'description': 'Unable to find jwks key referenced in token'}, 401)

    try:
        payload = jwt_parser.decode(
            token,
            rsa_key,
            algorithms=jwt.algorithms,
            audience=jwt.audience,
            issuer=jwt.issuer
        )
    except Exception as exc:
        raise AuthError({'code': 'invalid_header',
                         'description':
                             'Unable to parse authentication'
                             ' token.'}, 401) from exc

    return payload
