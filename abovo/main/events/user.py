from flask_socketio import emit
from .. import sio
from ..services import user
from ..utils.model_schemes import UserSchema
from ..utils.event_decorators import auth


@sio.on('users/get')
@auth.authenticated_only
def on_users_collection_get(json=None):
    if json is None:
        json = dict()
    users_collection = user.get_users().all()
    schema = UserSchema(many=True)
    result = schema.dump(users_collection)

    emit('users/get', {
        'type': 'Success',
        'users': result
    })


@sio.on('user/get')
@auth.authenticated_only
def on_user_by_username_get(username, json=None):
    if json is None:
        json = dict()
    try:
        users_by_username = user.get_user(username)
    except user.UserDoesNotExist:
        emit('user/get', {
            'type': 'Failure',
            'failure': 'UserDoesNotExist',
            'message': 'user with this username does not exist'
        })
    else:
        schema = UserSchema()
        result = schema.dump(users_by_username)

        emit('user/get', {
            'type': 'Success',
            'user': result
        })


@sio.on('user/update')
@auth.authenticated_only
@auth.self_only('user/update')
def on_current_user_update(username, json=None):
    if json is None:
        json = dict()
    updated_user = user.update_user(username, **json)
    schema = UserSchema(many=True)
    result = schema.dump(updated_user)

    emit('user/update', {
        'type': 'Success',
        'user': result
    })
