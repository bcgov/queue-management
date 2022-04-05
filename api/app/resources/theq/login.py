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

from flask import abort, redirect, request, url_for, g
from flask_login import login_user, logout_user
from flask_restx import Resource
from app.models.theq import CSR
from qsystem import api, application
from app.auth.auth import jwt

# Defining String constants to appease SonarQube
admin_index_const = "admin.index"

@api.route("/login/", methods=["GET"])
class Login(Resource):
    auth_string = 'Unable to authenticate request. You must be signed in prior to authenticated to the admin pages'

    @jwt.requires_auth_cookie
    def get(self):
        claims = g.jwt_oidc_token_info

        if claims["preferred_username"]:
            csr = CSR.find_by_username(claims["preferred_username"])
            if csr:
                if csr.deleted is None:
                    csr.is_active = True
                else:
                    csr.is_active = False

                csr.is_authenticated = False
                csr.is_anonymous = False

                login_user(csr)
                if application.config['USE_HTTPS']:
                    return redirect(url_for(admin_index_const,
                                            _scheme=application.config['PREFERRED_URL_SCHEME'],
                                            _external=application.config['USE_HTTPS']))
                else:
                    return redirect(url_for(admin_index_const))
            else:
                return abort(401, self.auth_string)
        else:
            return abort(401, self.auth_string)


@api.route("/logout/", methods=["GET"])
class Logout(Resource):
    auth_string = 'Unable to authenticate request. You must be signed in prior to authenticated to the admin pages'

    def get(self):
        logout_user()
        if application.config['USE_HTTPS']:
            return redirect(url_for(admin_index_const,
                            _scheme=application.config['PREFERRED_URL_SCHEME'],
                            _external=application.config['USE_HTTPS']))
        else:
            return redirect(url_for(admin_index_const))
