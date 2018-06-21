from flask import request, jsonify, g
from flask_restplus import Resource
import sqlalchemy.orm
from qsystem import api, db, oidc, socketio
from app.auth import required_scope
from app.models import Citizen, CSR
from cockroachdb.sqlalchemy import run_transaction
import logging
from marshmallow import ValidationError, pre_load
from sqlalchemy import exc

@api.route("/citizens/", methods=['GET', 'POST'])
class CitizenList(Resource):

    @oidc.accept_token(require_token=True)
    def get(self):
        try:
            csr = CSR.query.filter_by(username=g.oidc_token_info['username']).first()
            citizens = Citizen.query.filter_by(office_id=csr.office_id).all()
            return api.marshal(citizens, Citizen.model), 200
        except exc.SQLAlchemyError as e:
            print (e)
            return {"message": "api is down"}, 500

    @oidc.accept_token(require_token=True)
    def post(self):
        json_data = request.get_json()
        if not json_data:
            return {"message": "No input data received for creating citizen"}, 400
        
        try:
            data = Citizen.load(json_data)
        except ValidationError as err:
            return {"message": err.messages}, 422

        citizen_id          = data['citizen_id']
        office_id           = data['office_id']
        ticket_number       = data['ticket_number']
        citizen_name        = data['citizen_name']
        citizen_comments    = data['citizen_comments']
        qt_xn_citizen       = data['qt_xn_citizen']
        cs_id               = data['cs_id']

        citizen = Citizen.query.filter_by(citizen_id=citizen_id)

        if citizen is None:
            citizen = Citizen(office_id=office_id,
                              ticket_number=ticket_number,
                              citizen_name=citizen_name,
                              citizen_comments=citizen_comments,
                              qt_xn_citizen=qt_xn_citizen,
                              cs_id=cs_id)
            sessionmaker = sqlalchemy.orm.sessionmaker(db.engine)
            run_transaction(sessionmaker, Citizen.save)
            #socketio.emit?
            return {"message": "Citizen successfully created."}, 201
        else:
            return {"message": "Citizen already exists"}, 409

    #def post_invite_citizen(self):
        #return

# LIST Specific Customer
@api.route("/citizens/${citizenID}/", methods=["GET"])
class CitizenDetail(Resource):
    
    #@oidc.accept_token(require_token=True)
    def get_single_citizen(self, id):
        try:
            csr = CSR.query.filter_by(username=g.oidc_token_info['username']).first()
            citizens = Citizen.query.filter_by(office_id=csr['office_id']).get(id)
            return api.marshal(citizen, Citizen.model), 200
        except exc.SQLAlchemy as e:
            return {"message": "api is down"}, 500

    def put_single_citizen(self, id):
        try:
            citizen = Citizen.get(id)
        except Citizen.DoesNotExist:
            return {"message": "Citizen could not be found"}, 404

        #CS ID is the only thing that can change here, find out how it transitions ie//logic or input provided
        return
