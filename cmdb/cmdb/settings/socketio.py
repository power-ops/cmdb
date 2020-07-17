import socketio

async_mode = None

SOCKETIO = socketio.Server(async_mode=async_mode)


@SOCKETIO.event
def my_event(sid, message):
    SOCKETIO.emit('my_response', {'data': message['data']}, room=sid)


@SOCKETIO.event
def my_broadcast_event(sid, message):
    SOCKETIO.emit('my_response', {'data': message['data']})


@SOCKETIO.event
def join(sid, message):
    SOCKETIO.enter_room(sid, message['room'])
    SOCKETIO.emit('my_response', {'data': 'Entered room: ' + message['room']},
                  room=sid)


@SOCKETIO.event
def leave(sid, message):
    SOCKETIO.leave_room(sid, message['room'])
    SOCKETIO.emit('my_response', {'data': 'Left room: ' + message['room']},
                  room=sid)


@SOCKETIO.event
def close_room(sid, message):
    SOCKETIO.emit('my_response',
                  {'data': 'Room ' + message['room'] + ' is closing.'},
                  room=message['room'])
    SOCKETIO.close_room(message['room'])


@SOCKETIO.event
def my_room_event(sid, message):
    SOCKETIO.emit('my_response', {'data': message['data']}, room=message['room'])


@SOCKETIO.event
def disconnect_request(sid):
    SOCKETIO.disconnect(sid)


@SOCKETIO.event
def connect(sid, environ):
    SOCKETIO.emit('my_response', {'data': 'Connected', 'count': 0}, room=sid)


@SOCKETIO.event
def disconnect(sid):
    print('Client disconnected')


