from flask import request, jsonify, g
from flask_restplus import Resource
import sqlalchemy.orm
from qsystem import api, db, oidc, socketio

from app.auth import required_scope
from app.models import Citizen, User

from cockroachdb.sqlalchemy import run_transaction

import logging

@api.route("/citizens/<int:id>/")
class CitizenDetail(Resource):
    
    def get(self, id):
        citizen = Citizen.get_by_id(id)

        return api.marshal(citizen, Citizen.model), 200

    def delete(self, id):
        Citizen.query.filter_by(citizen_id=id).delete()
        db.session.commit()

        return '', 204
