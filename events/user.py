from app import socketio


@socketio.on('get_user')
def connect(username, password):
    pass