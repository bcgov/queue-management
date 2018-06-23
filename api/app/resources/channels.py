from flask import request, jsonify, g
from flask_restplus import Resource
import sqlalchemy.orm
from qsystem import api, db, oidc, socketio
from app.auth import required_scope
from app.models import Channel
from cockroachdb.sqlalchemy import run_transaction
import logging
from app.schemas import ChannelSchema
from sqlalchemy import exc

@api.route("/channels/", methods=["GET"])
class ChannelList(Resource):

    channels_schema =  ChannelSchema(many=True)

    #@oidc.accept_token(require_token=True)
    def get(self):
        try:
            channels = Channel.query.all()
            result = self.channels_schema.dump(channels)

            return jsonify({'channels': result})
        except exc.SQLAlchemyError as e:
            return {"message": "api is down"}, 500
