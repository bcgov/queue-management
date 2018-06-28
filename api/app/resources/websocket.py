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
from app.models import CSR
from qsystem import oidc, socketio


@socketio.on('myEvent')
def test_message(message):
    emit('myResponse', {'data': 'got it!', 'count': message['count']})


@socketio.on('joinRoom')
def on_join(message):
    cookie = request.cookies.get("oidc-jwt", None)
    if cookie is None:
        print("cookie is none")
        emit('joinRoomFail', {"sucess": False})
        return

    print(cookie)

    if not oidc.validate_token(cookie):
        print("Cookie failed validation")
        emit('joinRoomFail', {"sucess": False})
        return

    print("Validated")

    claims = jwt.get_unverified_claims(cookie)
    print(claims)

    username = claims["preferred_username"]
    csr = CSR.query.filter_by(username=username).first()
    if csr:
        print("Joining room")
        join_room(csr.office_id)
        emit('joinRoomSuccess', {"sucess": True})
        emit('update_customer_list', {"sucess": True}, room=csr.office_id)
        print("Success")
    else:
        print("Fail")
        emit('joinRoomFail', {"sucess": False})
