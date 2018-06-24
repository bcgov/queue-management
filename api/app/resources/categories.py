from flask import request, jsonify, g
from flask_restplus import Resource
import sqlalchemy.orm
from qsystem import api, db, oidc, socketio
from app.auth import required_scope
from app.models import Service
from cockroachdb.sqlalchemy import run_transaction
import logging
from sqlalchemy import exc
from app.schemas import ServiceSchema

@api.route("/categories/", methods=["GET"])
class Categories(Resource):

    categories_schema = ServiceSchema(many=True) 

    @oidc.accept_token(require_token=True)
    def get(self):
        try:
            services = Service.query.filter_by(actual_service_ind=0).all()
            result =  self.categories_schema.dump(services)
            return jsonify({'categories': result})

        except exc.SQLAlchemyError as e:
            print (e)
            return {"message": "api is down"}, 500