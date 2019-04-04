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

from flask import g, request
from flask_restplus import Resource
from marshmallow import ValidationError
from qsystem import api, api_call_with_retry, db, jwt, cache, socketio
from app.models.theq import CSR
from app.schemas.theq import CSRSchema


@api.route("/csrs/<int:id>/", methods=["PUT"])
class Services(Resource):

    csr_schema = CSRSchema()

    @jwt.requires_auth
    @api_call_with_retry
    def put(self, id):
        json_data = request.get_json()

        if not json_data:
            return {'message': 'No input data received for updating CSR'}, 400

        auth_csr = CSR.find_by_username(g.jwt_oidc_token_info['preferred_username'])
        edit_csr = CSR.query.filter_by(csr_id=id).first_or_404()

        if auth_csr.csr_id != edit_csr.csr_id:
            return {'message': 'You do not have permission to edit this CSR'}, 403

        try:
            edit_csr = self.csr_schema.load(json_data, instance=edit_csr, partial=True).data
        except ValidationError as err:
            return {'message': err.messages}, 422

        db.session.add(edit_csr)
        db.session.commit()

        result = self.csr_schema.dump(edit_csr)
        socketio.emit('csr_update', \
                      { "csr_id": edit_csr.csr_id, \
                        "receptionist_ind" : edit_csr.receptionist_ind }, \
                      room=auth_csr.office_id)

        # Purge cache of old CSR record so the new one can be fetched by the next request for it.
        CSR.delete_user_cache(g.jwt_oidc_token_info['preferred_username'])

        return {'service_request': result.data,
                'errors': result.errors}, 200
