from flask import session
from flask_socketio import SocketIO, emit, join_room, leave_room

socketio = SocketIO()

@socketio.on('joined', namespace='/chat')
def text(message):
    emit('status', {'socket msg': message})