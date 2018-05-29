from flask import abort, request, jsonify, g
from flask_login import current_user
from flask_restplus import Resource
from sqlalchemy import text, exc
from qsystem import api, db, socketio

from app.auth import login_required
from app.models import Client

import logging

@api.route("/clients/")
class ClientList(Resource):

    @api.marshal_with(Client.model)
    @login_required
    def get(self):
        try:
            clients = Client.query.filter_by(office_id=current_user.office_id).all()
            return clients, 200
        except exc.SQLAlchemyError as e:
            print(e)
            abort(500, sql_error=e)

    @api.marshal_with(Client.model)
    @login_required
    def post(self):
        json_input = request.get_json()
        name = json_input.get('name', None)

        if name == None:
            return {"message": "name is required"}, 400

        try:
            client = Client(name=name, office_id=current_user.office_id)
            db.session.add(client)
            db.session.commit()

            socketio.emit('update_customer_list', {"data": "test"}, room=current_user.office_id)
            return client, 201
        except exc.SQLAlchemyError as e:
            print(e)
            abort(500, sql_error=e)

@api.route("/clients/<int:id>/")
class ClientDetail(Resource):
    
    @api.marshal_with(Client.model)
    @login_required
    def get(self, id):
        try:
            client = Client.query.filter_by(id=id, office_id=current_user.office_id).first_or_404()

            emit('update_customer_list', {}, room="{office}".format(office=current_user.office_id))
            return client, 200
        except exc.SQLAlchemyError as e:
            print(e)
            abort(500, sql_error=e)

    @login_required
    def delete(self, id):
        try:
            Client.query.filter_by(id=id, office_id=current_user.office_id).delete()
            db.session.commit()

            socketio.emit('update_customer_list', {"data": "test"}, room=current_user.office_id)
            return '', 204
        except exc.SQLAlchemyError as e:
            print(e)
            abort(500, sql_error=e)

