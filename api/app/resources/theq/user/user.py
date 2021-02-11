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

from flask import g, request
from flask_restx import Resource
from sqlalchemy import exc

from app.models.theq import PublicUser as PublicUserModel
from app.schemas.theq import UserSchema
from qsystem import api, db
from app.utilities.auth_util import Role, has_any_role
from app.auth.auth import jwt


@api.route("/users/", methods=['POST'])
class PublicUsers(Resource):
    user_schema = UserSchema(many=False)

    @jwt.has_one_of_roles([Role.online_appointment_user.value])
    def post(self):
        try:
            user_info = g.jwt_oidc_token_info
            user: PublicUserModel = PublicUserModel.find_by_username(user_info.get('username'))
            if not user:
                user = PublicUserModel()
                user.username = user_info.get('username')
                user.email = user_info.get('email')
            else:  # update email only if the email is None for existing user
                if not user.email:
                    user.email = user_info.get('email')
            user.display_name = user_info.get('display_name')
            user.last_name = user_info.get('last_name')
            db.session.add(user)
            db.session.commit()

            result = self.user_schema.dump(user)
            return result, 200

        except exc.SQLAlchemyError as e:
            print(e)
            return {'message': 'API is down'}, 500


@api.route("/users/<int:user_id>/", methods=['PUT'])
class PublicUser(Resource):
    user_schema = UserSchema(many=False)

    @jwt.has_one_of_roles([Role.online_appointment_user.value])
    def put(self, user_id: int):
        try:
            json_data = request.get_json()
            user_info = g.jwt_oidc_token_info
            user: PublicUserModel = PublicUserModel.find_by_username(user_info.get('username'))
            user.email = json_data.get('email')
            user.telephone = json_data.get('telephone')
            user.send_reminders = json_data.get('send_reminders')
            db.session.add(user)
            db.session.commit()

            result = self.user_schema.dump(user)
            return result, 200

        except exc.SQLAlchemyError as e:
            print(e)
            return {'message': 'API is down'}, 500


@api.route("/users/me/", methods=['GET'])
class CurrentUser(Resource):
    user_schema = UserSchema(many=False)

    @jwt.has_one_of_roles([Role.online_appointment_user.value])
    def get(self):
        try:
            user_info = g.jwt_oidc_token_info
            user: PublicUserModel = PublicUserModel.find_by_username(user_info.get('username'))

            result = self.user_schema.dump(user)
            return result, 200

        except exc.SQLAlchemyError as e:
            print(e)
            return {'message': 'API is down'}, 500


