from flask_login import current_user
from flask_socketio import emit, join_room

from app.models import Client
from qsystem import socketio

@socketio.on('myEvent')
def test_message(message):
    emit('myResponse', {'data': 'got it!', 'count': message['count']})

@socketio.on('joinRoom')
def on_join(message):    
    if current_user.is_authenticated:
        join_room(current_user.office_id)
        emit('joinRoomSuccess', {'data': "{user} has joined the room".format(user=current_user.username)})
        emit('update_customer_list', {"data": "test"}, room=current_user.office_id)
    else:
        emit('joinRoomFail', {'data': "{user} failed to join the room".format(user=current_user.username)})

@socketio.on('pingRoom')
def ping_room(message):
    if current_user.is_authenticated:
        emit('ping_room', {'data': "{user} has pinged the room".format(user=current_user.username)}, room=current_user.office_id)
    else:
        emit('joinRoomFail', {'data': "{user} failed to join the room".format(user=current_user.username)})
