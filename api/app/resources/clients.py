from flask import request, jsonify, g
from flask_login import current_user
from flask_restplus import Resource, abort
import sqlalchemy.orm
from qsystem import api, db, socketio

from app.auth import login_required
from app.models import Client

from cockroachdb.sqlalchemy import run_transaction

import logging

@api.route("/clients/")
class ClientList(Resource):

    @login_required
    @api.marshal_with(Client.model)
    def get(self):
        clients = Client.query.filter_by(office_id=current_user.office_id).all()
        return clients, 200

    @login_required
    def post(self):
        json_input = request.get_json()
        name = json_input.get('name', None)

        if name == None:
            return {"message": "name is required"}, 400

        client = Client(name=name, office_id=current_user.office_id)
        sessionmaker = sqlalchemy.orm.sessionmaker(db.engine)
        run_transaction(sessionmaker, client.save_to_db)

        socketio.emit('update_customer_list', {"data": "test"}, room=current_user.office_id)
        return client, 201

@api.route("/clients/<int:id>/")
class ClientDetail(Resource):
    
    @login_required
    @api.marshal_with(Client.model)
    def get(self, id):
        client = Client.query.filter_by(id=id, office_id=current_user.office_id).first_or_404()

        emit('update_customer_list', {}, room="{office}".format(office=current_user.office_id))
        return client, 200

    @login_required
    def delete(self, id):
        Client.query.filter_by(id=id, office_id=current_user.office_id).delete()
        db.session.commit()

        socketio.emit('update_customer_list', {"data": "test"}, room=current_user.office_id)
        return '', 204
