from flask import request, jsonify, g
from flask_restplus import Resource, abort
import sqlalchemy.orm
from qsystem import api, db, oidc, socketio

from app.auth import required_scope
from app.models import Client, User

from cockroachdb.sqlalchemy import run_transaction

import logging

@api.route("/clients/")
class ClientList(Resource):

    @api.marshal_with(Client.model)
    @oidc.accept_token(require_token=True)
    def get(self):
        user = User.query.filter_by(username=g.oidc_token_info['username']).first()
        clients = Client.query.filter_by(office_id=user.office_id).all()
        return clients, 200

    @api.marshal_with(Client.model)
    @oidc.accept_token(require_token=True)
    def post(self):
        user = User.query.filter_by(username=g.oidc_token_info['username']).first()
        json_input = request.get_json()
        name = json_input.get('name', None)

        if name == None:
            return {"message": "name is required"}, 400

        client = Client(name=name, office_id=user.office_id)
        sessionmaker = sqlalchemy.orm.sessionmaker(db.engine)
        run_transaction(sessionmaker, client.save_to_db)

        socketio.emit('update_customer_list', {}, room=user.office_id)
        return 201

@api.route("/clients/<int:id>/")
class ClientDetail(Resource):
    
    @api.marshal_with(Client.model)
    @oidc.accept_token(require_token=True)
    def get(self, id):
        user = User.query.filter_by(username=g.oidc_token_info['username']).first()
        client = Client.query.filter_by(id=id, office_id=user.office_id).first_or_404()

        emit('update_customer_list', {}, room="{office}".format(office=user.office_id))
        return client, 200

    @oidc.accept_token(require_token=True)
    def delete(self, id):
        user = User.query.filter_by(username=g.oidc_token_info['username']).first()
        Client.query.filter_by(id=id, office_id=user.office_id).delete()
        db.session.commit()

        socketio.emit('update_customer_list', {}, room=user.office_id)
        return '', 204
