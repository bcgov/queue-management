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
from flask_socketio import emit, join_room

from app.auth.auth import jwt
from app.models.theq import CSR, Office
from app.utilities.auth_util import get_username
from qsystem import socketio, my_print
from flask_jwt_oidc.exceptions import AuthError


@socketio.on('joinRoom')
@jwt.requires_auth_cookie
def on_join(message):
    username = get_username()
    if username != '':
        my_print("==> In Python, @socketio.on('joinRoom'): username is: " +
            username)
        csr = CSR.find_by_username(username)
        if csr:
            join_room(csr.office.office_name)
            logging.info("==> In websocket.py, CSR joinroom, CSR:  %s ; request sid: %s", csr.username, str(request.sid))
            emit('joinRoomSuccess', {"sucess": True})
            emit('get_Csr_State_IDs', {"success": True})
            emit('update_customer_list', {"success": True})
        else:
            logging.info("Fail")
            emit('joinRoomFail', {"success": False})
    else:
        logging.info("No username on request")
        emit('joinRoomFail', {"success": False})


@socketio.on('joinSmartboardRoom')
def on_join_smartboard(message):
    try:
        office_id = int(message['office_id'])
        room = "sb-%s" % office_id

        my_print("Joining room: %s" % room)

        join_room(room)
        logging.info("==> In websocket.py, Smartboard joinroom, Office id: %s ; request sid: %s" , str(office_id), str(request.sid))
        emit('joinSmartboardRoomSuccess')
    except KeyError as exception:
        logging.exception(exception)
        emit('joinSmartboardRoomFail', {"sucess": False, "message": "office_id must be passed to this method"})

    except ValueError as exception:
        logging.exception(exception)
        emit('joinSmartboardRoomFail', {"sucess": False, "message": "office_id must be an integer"})


@socketio.on('clear_csr_user_id')
def clear_csr_user_id(csr_id):
    CSR.update_user_cache(csr_id)


@socketio.on('sync_offices_cache')
def sync_offices_cache():
    Office.clear_offices_cache()


@socketio.on_error()
def error_handler(e):
    # Passing the execution as it would be an auth error with invalid token.
    logging.error('Socket error %s', e)
