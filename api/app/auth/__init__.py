"""Keycloak Auth Services
"""

from functools import wraps
import json
import logging
from qsystem import api

from flask import request, jsonify
from jose import jwt

def get_token_auth_header():
    """Obtains the access token from the Authorization Header
    """
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise AuthError({"code": "authorization_header_missing",
                        "description": "Authorization header is expected"}, 401)

    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise AuthError({"code": "invalid_header",
                        "description": "Authorization header must start with Bearer"}, 401)
    elif len(parts) == 1:
        raise AuthError({"code": "invalid_header", "description": "Token not found"}, 401)
    elif len(parts) > 2:
        raise AuthError({"code": "invalid_header",
                        "description": "Authorization header must be Bearer token"}, 401)

    token = parts[1]
    return token

def required_scope(required_scope):
    """Determines if the required scope is present in the access token
    Args:
        required_scope (str): The scope required to access the resource
    """
    token = get_token_auth_header()
    unverified_claims = jwt.get_unverified_claims(token)

    if unverified_claims.get('realm_access'):
        roles = unverified_claims.get('realm_access').get('roles')
        if roles and required_scope in roles:
            return True

    return False
