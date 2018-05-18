from flask import request, jsonify, g
from flask_restplus import Resource
from sqlalchemy import text, exc
from qsystem import api, db
from app.models import Note

import logging

@api.route("/notes/")
class Notes(Resource):

    @staticmethod
    def get():
        try:
            notes = db.session.query(Note).all()
            return {"notes": notes}, 200
        except exc.SQLAlchemyError as e:
            print(e)
            return {"message": "api is down"}, 500

    def create(self, data):
        json_input = request.get_json()
        notes_value = json_input.get('notes_value', None)

        if notes_value == None:
            return {"message": "notes_value is required"}, 400

        try:
            note = Note(value=notes_value)
            db.session.add(note)
            return {"note": note}, 201
        except exc.SQLAlchemyError as e:
            print(e)
            return {"message": "api is down"}, 500 
