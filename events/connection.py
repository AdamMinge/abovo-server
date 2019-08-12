from app import socketio
from models import UserModel
from utils.model_queries import user
from flask_socketio import ConnectionRefusedError


@socketio.on('connect')
def connect(username, password):
    current_user = user.get_user(username)

    if not UserModel.verify_hash(password, current_user.password):
        raise ConnectionRefusedError("Wrong credentials")


@socketio.on('disconnect')
def disconnect():
    pass
