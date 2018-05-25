from flask_login import current_user
from flask_socketio import emit, join_room

from app.models import Client
from qsystem import socketio

@socketio.on('my event')
def test_message(message):
	print("Receiving message")
	print(message)
    emit('my response', {'data': 'got it!', 'count': message['count']})
    print("Pinging back")

@socketio.on('join')
def join_room(message):    
    print("Received request to join room")
    if current_user.is_authenticated:
        print("{user} is attempting to join room: {room}".format(user=current_user.username, room=current_user.office_id))
        join_room(current_user.office_id)
        emit('joined', {'data': "{user} has joined the room".format(user=current_user.username)})
    else:
        print ("Join failed as user is not authed")
        emit('join_fail', {'data': "{user} failed to join the room".format(user=current_user.username)})
