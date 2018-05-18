from flask_socketio import emit

from app.models import Client
from qsystem import socketio

@socketio.on('my event')
def test_message(message):
    emit('my response', {'data': 'got it!', 'count': message['count']})
