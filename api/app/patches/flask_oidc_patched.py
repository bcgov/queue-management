from flask_oidc import OpenIDConnect as OriginalOIDC, _json_loads
from flask import current_app
from base64 import b64encode
import certifi
from six.moves.urllib.parse import urlencode
from qsystem import cache
import time

import httplib2


class OpenIDConnect(OriginalOIDC):

    @cache.memoize(timeout=300)
    def _get_token_info(self, token):
        start_time = time.time()
        # We hard code to use client_secret_post, because that's what the Google
        # oauth2client library defaults to
        request = {'token': token}
        headers = {'Content-type': 'application/x-www-form-urlencoded'}

        hint = current_app.config['OIDC_TOKEN_TYPE_HINT']
        if hint != 'none':
            request['token_type_hint'] = hint

        auth_method = current_app.config['OIDC_INTROSPECTION_AUTH_METHOD']
        if auth_method == 'client_secret_basic':
            basic_auth_string = '%s:%s' % (self.client_secrets['client_id'], self.client_secrets['client_secret'])
            basic_auth_bytes = bytearray(basic_auth_string, 'utf-8')
            headers['Authorization'] = 'Basic %s' % b64encode(basic_auth_bytes)
        elif auth_method == 'bearer':
            headers['Authorization'] = 'Bearer %s' % token
        elif auth_method == 'client_secret_post':
            request['client_id'] = self.client_secrets['client_id']
            request['client_secret'] = self.client_secrets['client_secret']

        # Use separate certs to get around python 3.4 cert issues
        resp, content = httplib2.Http(ca_certs=certifi.where()) \
            .request(self.client_secrets['token_introspection_uri'], 'POST', urlencode(request), headers=headers)

        total_time = time.time() - start_time

        if total_time > 1:
            print("Sending request to OIDC server in %.3fs" % total_time)

        return _json_loads(content)
