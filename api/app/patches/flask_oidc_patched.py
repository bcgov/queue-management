"""Patching the FLASK-OIDC module to turn off Certificate Validation
   This seems to be an issue only with wildcard* certs.
   TODO: Check the upstream libraries for when this issue is fixed
   TODO: Before the project completes, create a patch and submit upstream NOT ON THIS, but on handling wildcard certs
"""
from flask_oidc import OpenIDConnect as OriginalOIDC, _json_loads
from flask import request, session, redirect, url_for, g, current_app
from base64 import b64encode, urlsafe_b64encode, urlsafe_b64decode
from six.moves.urllib.parse import urlencode
from qsystem import cache
import time

import httplib2
import logging

class OpenIDConnect(OriginalOIDC):

    @cache.memoize(timeout=60)
    def _get_token_info(self, token):
        start_time = time.time()
        # We hardcode to use client_secret_post, because that's what the Google
        # oauth2client library defaults to
        request = {'token': token}
        headers = {'Content-type': 'application/x-www-form-urlencoded'}

        hint = current_app.config['OIDC_TOKEN_TYPE_HINT']
        if hint != 'none':
            request['token_type_hint'] = hint

        auth_method = current_app.config['OIDC_INTROSPECTION_AUTH_METHOD']
        if (auth_method == 'client_secret_basic'):
            basic_auth_string = '%s:%s' % (self.client_secrets['client_id'], self.client_secrets['client_secret'])
            basic_auth_bytes = bytearray(basic_auth_string, 'utf-8')
            headers['Authorization'] = 'Basic %s' % b64encode(basic_auth_bytes)
        elif (auth_method == 'bearer'):
            headers['Authorization'] = 'Bearer %s' % token
        elif (auth_method == 'client_secret_post'):
            request['client_id'] = self.client_secrets['client_id']
            request['client_secret'] = self.client_secrets['client_secret']

        # as of Python 3.4 disable_ssl_certificate_validation defaults to False,
        # this causes wildcard certs to throw errors,
        # and we use wildcards on our KeyCloak server, which throws errors for token verification calls
        # TODO: (Remove this whole patch) - This line of code is a temporary workaround for wildcard cert errors
        resp, content = httplib2.Http(disable_ssl_certificate_validation=True).request(
            self.client_secrets['token_introspection_uri'], 'POST',
            urlencode(request), headers=headers)

        total_time = time.time() - start_time
        print ("Sending request to OIDC server in %.3fs" % total_time)

        # TODO: Cache this reply
        return _json_loads(content)
