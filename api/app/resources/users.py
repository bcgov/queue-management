from flask import request, jsonify, g
from flask_restplus import Resource
from flask_socketio import emit
from sqlalchemy import text, exc
from qsystem import api, db

from app.models import User

import logging

@api.route("/users/me/")
class UserMe(Resource):

    @api.marshal_with(User.model)
    def get(self):
        try:
            return '', 200
        except exc.SQLAlchemyError as e:
            print(e)
            return {"message": "api is down"}, 500
