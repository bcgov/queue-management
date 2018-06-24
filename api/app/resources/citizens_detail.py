from flask import request, jsonify, g
from flask_restplus import Resource
import sqlalchemy.orm
from qsystem import api, db, oidc, socketio
from app.auth import required_scope
from app.models import Citizen, CSR, CitizenState
from cockroachdb.sqlalchemy import run_transaction
import logging
from marshmallow import ValidationError, pre_load
from app.schemas import CitizenSchema
from sqlalchemy import exc

@api.route("/citizens/<int:id>/", methods=["GET","PUT"])
class CitizenDetail(Resource):
    
    citizen_schema = CitizenSchema()

    @oidc.accept_token(require_token=True)
    def get(self, id):
        try:
            csr = CSR.query.filter_by(username=g.oidc_token_info['username']).first()
            citizen = Citizen.get_by_id(id)
            result = self.citizen_schema.dump(citizen)
            return jsonify({'citizen': result})

        except exc.SQLAlchemyError as e:
            print (e)
            return {"message": "api is down"}, 500

    @oidc.accept_token(require_token=True)
    def put(self, id):
        json_data = request.get_json()
        
        if not json_data:
            return {"message": "No input data received for creating citizen"}, 400
        
        csr = CSR.query.filter_by(username=g.oidc_token_info['username']).first()
        citizen = Citizen.get_by_id(id, True)
        
        try:
            data = self.citizen_schema.load(json_data, instance=citizen, partial=True).data

        except ValidationError as err:
            return {"message": err.messages}, 422

        citizen.save()
        return {"message": "Citizen successfully created."}, 201
