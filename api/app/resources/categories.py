from flask import request, jsonify, g
from flask_restplus import Resource
import sqlalchemy.orm
from qsystem import api, db, oidc, socketio
from app.auth import required_scope
from app.models import Service
from cockroachdb.sqlalchemy import run_transaction
import logging
from sqlalchemy import exc

# LIST Service Catagories Specifically
@api.route("/categories/", methods=["GET"])
class Catagories(Resource):

    @oidc.accept_token(require_token=True)
    def get(self):
        try:
            services = Service.query.filter_by(actual_service=0).all()
            return api.marshal(services, Service.model), 200
        except exc.SQLAlchemyError as e:
            return {"message": "api is down"}, 500