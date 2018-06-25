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

from flask import request, jsonify, g
from flask_restplus import Resource
import sqlalchemy.orm
from qsystem import api, db, oidc, socketio
from app.auth import required_scope
from app.models import Citizen, CSR, CitizenState
from cockroachdb.sqlalchemy import run_transaction
import logging
from marshmallow import ValidationError, pre_load
from app.models import ServiceReq, SRState
from app.schemas import CitizenSchema, ServiceReqSchema
from sqlalchemy import exc

@api.route("/citizens/<int:id>/", methods=["GET","PUT"])
class CitizenDetail(Resource):
    
    citizen_schema = CitizenSchema()

    @oidc.accept_token(require_token=True)
    def get(self, id):
        try:
            csr = CSR.query.filter_by(username=g.oidc_token_info['username']).first()
            #csr = CSR.query.filter_by(username='adamkroon').first()
            citizen = Citizen.query.get(id)
            result = self.citizen_schema.dump(citizen)
            return {'citizen': result.data,
                    'errors': result.errors}

        except exc.SQLAlchemyError as e:
            print (e)
            return {'message': 'API is down'}, 500

    @oidc.accept_token(require_token=True)
    def put(self, id):
        json_data = request.get_json()
        
        if not json_data:
            return {'message': 'No input data received for updating citizen'}, 400
        
        csr = CSR.query.filter_by(username=g.oidc_token_info['username']).first()
        #csr = CSR.query.filter_by(username='adamkroon').first()
        citizen = Citizen.query.get(id)
        
        try:
            citizen = self.citizen_schema.load(json_data, instance=citizen, partial=True).data

        except ValidationError as err:
            return {'message': err.messages}, 422

        db.session.add(citizen)
        db.session.commit()

        result = self.citizen_schema.dump(citizen)
        return {'citizen': result.data, 'errors': result.errors}, 200

@api.route("/citizens/<int:id>/add_to_queue/", methods=["POST"])
class CitizenAddToQueue(Resource):

    citizen_schema = CitizenSchema()

    @oidc.accept_token(require_token=True)
    def post(self, id):
        csr = CSR.query.filter_by(username=g.oidc_token_info['username']).first()
        #csr = CSR.query.filter_by(username='adamkroon').first()
        citizen = Citizen.query.get(id)

        active_service_request = citizen.get_active_service_request()

        if active_service_request == None:
            return {"message": "Citizen has no active service requests"}

        active_service_request.add_to_queue(csr)

        pending_service_state = SRState.query.filter_by(sr_code='Pending').first()
        active_service_request.sr_state_id = pending_service_state.sr_state_id

        db.session.add(active_service_request)
        db.session.commit()

        result = self.citizen_schema.dump(citizen)
        return {'citizen': result.data, 'errors': result.errors}, 200

@api.route("/citizens/<int:id>/invite/", methods=["POST"])
class CitizenInvite(Resource):

    citizen_schema = CitizenSchema()

    @oidc.accept_token(require_token=True)
    def post(self, id):
        csr = CSR.query.filter_by(username=g.oidc_token_info['username']).first()
        #csr = CSR.query.filter_by(username='adamkroon').first()
        citizen = Citizen.query.get(id)
        active_service_request = citizen.get_active_service_request()

        if active_service_request == None:
            return {"message": "Citizen has no active service requests"}

        active_service_request.invite(csr)

        pending_service_state = SRState.query.filter_by(sr_code='Pending').first()
        active_service_request.sr_state_id = pending_service_state.sr_state_id

        db.session.add(active_service_request)
        db.session.commit()

        result = self.citizen_schema.dump(citizen)
        return {'citizen': result.data, 'errors': result.errors}, 200

@api.route("/citizens/<int:id>/begin_service/", methods=["POST"])
class CitizenBeginService(Resource):

    citizen_schema = CitizenSchema()

    @oidc.accept_token(require_token=True)
    def post(self, id):
        csr = CSR.query.filter_by(username=g.oidc_token_info['username']).first()
        #csr = CSR.query.filter_by(username='adamkroon').first()
        citizen = Citizen.query.get(id)
        active_service_request = citizen.get_active_service_request()

        if active_service_request == None:
            return {"message": "Citizen has no active service requests"}

        active_service_request.begin_service(csr)
        pending_service_state = SRState.query.filter_by(sr_code='Active').first()
        active_service_request.sr_state_id = pending_service_state.sr_state_id

        db.session.add(active_service_request)
        db.session.commit()

        result = self.citizen_schema.dump(citizen)
        return {'citizen': result.data, 'errors': result.errors}, 200

@api.route("/citizens/<int:id>/finish_service/", methods=["POST"])
class CitizenFinishService(Resource):

    citizen_schema = CitizenSchema()

    @oidc.accept_token(require_token=True)
    def post(self, id):
        csr = CSR.query.filter_by(username=g.oidc_token_info['username']).first()
        #csr = CSR.query.filter_by(username='adamkroon').first()
        citizen = Citizen.query.get(id)
        active_service_request = citizen.get_active_service_request()

        if active_service_request == None:
            return {"message": "Citizen has no active service requests"}

        active_service_request.finish_service(csr)
        citizen_state = CitizenState.query.filter_by(cs_state_name="Received Services").first()
        citizen.cs_id = citizen_state.cs_id

        pending_service_state = SRState.query.filter_by(sr_code='Complete').first()
        active_service_request.sr_state_id = pending_service_state.sr_state_id

        db.session.add(active_service_request)
        db.session.commit()

        result = self.citizen_schema.dump(citizen)
        return {'citizen': result.data, 'errors': result.errors}, 200

@api.route("/citizens/<int:id>/place_on_hold/", methods=["POST"])
class CitizenPlaceOnHold(Resource):

    citizen_schema = CitizenSchema()

    @oidc.accept_token(require_token=True)
    def post(self, id):
        csr = CSR.query.filter_by(username=g.oidc_token_info['username']).first()
        #csr = CSR.query.filter_by(username='adamkroon').first()
        citizen = Citizen.query.get(id)
        active_service_request = citizen.get_active_service_request()

        if active_service_request == None:
            return {"message": "Citizen has no active service requests"}

        active_service_request.place_on_hold(csr)
        pending_service_state = SRState.query.filter_by(sr_code='Active').first()
        active_service_request.sr_state_id = pending_service_state.sr_state_id

        db.session.add(active_service_request)
        db.session.commit()

        result = self.citizen_schema.dump(citizen)
        return {'citizen': result.data, 'errors': result.errors}, 200

@api.route("/citizens/<int:id>/service_requests/", methods=["GET"])
class CitizenServiceRequests(Resource):

    service_requests_schema = ServiceReqSchema(many=True)

    @oidc.accept_token(require_token=True)
    def get(self, id):
        try:
            csr = CSR.query.filter_by(username=g.oidc_token_info['username']).first()
            #csr = CSR.query.filter_by(username='adamkroon').first()
            citizen = Citizen.query.get(id)
            result = self.service_requests_schema.dump(citizen.service_reqs)
            return {'service_requests': result.data,
                    'errors': result.errors}

        except exc.SQLAlchemyError as e:
            print (e)
            return {'message': 'API is down'}, 500