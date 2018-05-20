from flask import request, jsonify, g
from flask_restplus import Resource
from sqlalchemy import text, exc
from qsystem import api, db

from app.auth import login_required
from app.models import Office

import logging

@api.route("/offices/")
class OfficeList(Resource):

    @api.marshal_with(Office.model)
    @login_required
    def get(self):
        try:
            offices = Office.query.all()
            return offices, 200
        except exc.SQLAlchemyError as e:
            print(e)
            return {"message": "api is down"}, 500

    @api.marshal_with(Office.model)
    @login_required
    def post(self, data):
        json_input = request.get_json()
        name = json_input.get('name', None)

        if name == None:
            return {"message": "name is required"}, 400

        try:
            office = Office(name=name)
            db.session.add(office)
            return office, 201
        except exc.SQLAlchemyError as e:
            print(e)
            return {"message": "api is down"}, 500 

@api.route("/offices/<int:id>/")
class OfficeDetail(Resource):
    
    @api.marshal_with(Office.model)
    @login_required
    def get(self, id):
        try:
            office = Office.query.filter_by(id=id).first()

            return office, 200
        except exc.SQLAlchemyError as e:
            print(e)
            return {"message": "api is down"}, 500

    @login_required
    def destroy(self, id):
        try:
            Office.query.filter_by(id=id).first().delete()
            
            return '', 204
        except exc.SQLAlchemyError as e:
            print(e)
            return {"message": "api is down"}, 500
