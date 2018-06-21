from flask import request, g
from flask_socketio import emit, join_room
from jose import jwt

#from app.models import User
from qsystem import oidc, socketio

@socketio.on('myEvent')
def test_message(message):
    emit('myResponse', {'data': 'got it!', 'count': message['count']})

@socketio.on('joinRoom')
def on_join(message):
    cookie = request.cookies.get("oidc-jwt", None)
    if cookie == None:
        print("cookie is none")
        emit('joinRoomFail', {})
        return

    print(cookie)

    if not oidc.validate_token(cookie):
        print("Cookie failed validation")
        emit('joinRoomFail', {})
        return

    print("Validated")

    claims = unverified_claims = jwt.get_unverified_claims(cookie)
    print(claims)

    username = claims["preferred_username"]
    user = User.query.filter_by(username=username).first()
    print (user)
    if user:
        join_room(user.office_id)
        emit('joinRoomSuccess', {})
        emit('update_customer_list', {}, room=user.office_id)
    else:
        emit('joinRoomFail', {})
