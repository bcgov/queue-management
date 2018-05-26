from flask_login import current_user
from flask_socketio import emit, join_room

from app.models import Client
from qsystem import socketio

@socketio.on('myEvent')
def test_message(message):
    print("Receiving message")
    print(message)
    emit('myResponse', {'data': 'got it!', 'count': message['count']})
    print("Pinging back")

@socketio.on('joinRoom')
def on_join(message):    
    print("Received request to join room")
    print(message)
    if current_user.is_authenticated:
        print("{user} is attempting to join room: {room}".format(user=current_user.username, room=current_user.office_id))
        join_room("vancouver")
        emit('joinRoomSuccess', {'data': "{user} has joined the room".format(user=current_user.username)})
    else:
        print ("Join failed as user is not authed")
        emit('joinRoomFail', {'data': "{user} failed to join the room".format(user=current_user.username)})
