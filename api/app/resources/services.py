from flask import request, jsonify, g
from flask_restplus import Resource
import sqlalchemy.orm
from qsystem import api, db, oidc, socketio
from app.auth import required_scope
from app.models import Service
from app.models import Office
from cockroachdb.sqlalchemy import run_transaction
import logging
from sqlalchemy import exc
from app.schemas import ServiceSchema

@api.route("/services/", methods=["GET"])
class Services(Resource):

    service_schema = ServiceSchema(many=True)
    services_schema =  ServiceSchema(many=True)

    #@oidc.accept_token(require_token=True)
    def get(self):
        if request.args.get('office_id'):
            try:
                office_id = int(request.args['office_id'])
                office = Office.query.get(office_id)
                services = office.services
                result = self.service_schema.dump(services)
                return jsonify({'services': result})
            except exc.SQLAlchemyError as e:
                print (e)
                return {"message": "api is down"}, 500
            except ValueError as e:
                return {"message": "office_id must be an integer."}, 400
        else:    
            try:
                services = Service.query.all()
                result = self.services_schema.dump(services)
                return jsonify({'services': result})
            except exc.SQLAlchemyError as e:
                print (e)
                return {"message": "api is down"}, 500

        #return api.marshal(services, Service.model), 200