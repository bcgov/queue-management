from flask import request, jsonify, g
from flask_login import current_user
from flask_restplus import Resource
from flask_socketio import emit
from sqlalchemy import text, exc
from qsystem import api, db

from app.auth import login_required
from app.models import User

import logging

@api.route("/users/me/")
class UserMe(Resource):

    @api.marshal_with(User.model)
    @login_required
    def get(self):
        try:
            print(current_user)
            print(current_user.office)
            return current_user, 200
        except exc.SQLAlchemyError as e:
            print(e)
            return {"message": "api is down"}, 500
