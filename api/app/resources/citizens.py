from flask import request, jsonify, g
from flask_restplus import Resource
import sqlalchemy.orm
from qsystem import api, db, oidc, socketio
from app.auth import required_scope
from app.models import Citizen, User
from cockroachdb.sqlalchemy import run_transaction
import logging
from marshmallow import ValidationError

@api.route("/citizens/")
class Citizen(Resource):

    #@oidc.accept_token(require_token=True)
    def get(self):
        try:
            citizens = Citizen.query.all()
            return api.marshal(citizens, Citizen.model), 200
        except exc.SQLAlchemyError as e:
            return {"message": "api is down"}, 500

# LIST Specific Customer
@api.route("/citizens/<int:id>/")
class CitizenDetail(Resource):
    
    @api.marshal_with(Citizen.model)
    def get(self, id):
        citizen = Citizen.get_by_id(id)
        return api.marshal(citizen, Citizen.model), 200