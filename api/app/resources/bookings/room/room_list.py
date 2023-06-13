'''Copyright 2018 Province of British Columbia

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.'''

import logging
from flask import request
from flask_restx import Resource
from sqlalchemy import exc
from app.models.bookings import Room
from app.models.theq import CSR
from app.schemas.bookings import RoomSchema
from qsystem import api
from app.utilities.auth_util import Role, get_username
from app.auth.auth import jwt


@api.route("/rooms/", methods=["GET"])
class RoomList(Resource):

    rooms_schema = RoomSchema(many=True)

    @jwt.has_one_of_roles([Role.internal_user.value])
    def get(self):

        csr = CSR.find_by_username(get_username())

        office_id = request.args.get('office_id', csr.office_id)
        try:
            rooms = Room.query.filter_by(office_id=office_id)\
                              .filter(Room.deleted.is_(None))
            result = self.rooms_schema.dump(rooms)
            return {'rooms': result,
                    'errors': self.rooms_schema.validate(rooms)}, 200

        except exc.SQLAlchemyError as error:
            logging.error(error, exc_info=True)
            return {"message": "api is down"}, 500
