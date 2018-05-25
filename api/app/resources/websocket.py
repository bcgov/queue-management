from flask_login import current_user
from flask_socketio import emit, join_room

from app.models import Client
from qsystem import socketio

@socketio.on('my event')
def test_message(message):
    emit('my response', {'data': 'got it!', 'count': message['count']})

@socketio.on('join')
def join_room(message):
    if current_user.is_authenticated:
        join_room(current_user.office_id)
        emit('joined', {'data': "{user} has joined the room".format(user=current_user.username)})
    else:
    	emit('join_fail', {'data': "{user} failed to join the room".format(user=current_user.username)})
