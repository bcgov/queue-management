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

from flask import request
from flask_socketio import emit, join_room
from jose import jwt
from app.models.theq import CSR
from qsystem import oidc, socketio
import json

@socketio.on('joinRoom')
def on_join(message):
    cookie = request.cookies.get("oidc-jwt", None)
    if cookie is None:
        emit('joinRoomFail', {"sucess": False})
        return

    if not oidc.validate_token(cookie):
        print("Cookie failed validation")
        emit('joinRoomFail', {"sucess": False})
        return

    claims = jwt.get_unverified_claims(cookie)

    if claims["preferred_username"]:
        csr = CSR.find_by_username(claims["preferred_username"])
        if csr:
            join_room(csr.office_id)
            emit('joinRoomSuccess', {"sucess": True})
            emit('get_Csr_State_IDs', {"success": True})
            emit('update_customer_list', {"success": True})
        else:
            print("Fail")
            emit('joinRoomFail', {"success": False})
    else:
        print("No preferred_username on request")
        emit('joinRoomFail', {"success": False})

@socketio.on('joinSmartboardRoom')
def on_join_smartboard(message):
    try:
        office_id = int(message['office_id'])
        room = "sb-%s" % office_id

        print("Joining room: %s" % room)

        join_room(room)
        emit('joinSmartboardRoomSuccess')
    except KeyError as e:
        print(e)
        emit('joinSmartboardRoomFail', {"sucess": False, "message": "office_id must be passed to this method"})

    except ValueError as e:
        print(e)
        emit('joinSmartboardRoomFail', {"sucess": False, "message": "office_id must be an integer"})

@socketio.on('clear_csr_user_id')
def clear_csr_user_id(csr_id):
    CSR.update_user_cache(csr_id)
