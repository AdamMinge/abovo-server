from flask import request
from flask_login import login_user, logout_user
from flask_socketio import emit
from flask_login import current_user
from ..models import UserModel
from ..utils.model_schemes import UserSchema
from ..services import user
from .. import sio, uts


@sio.on('login')
def on_login(json=None):
    if json is None:
        json = dict()
    try:
        username = json['username']
        password = json['password']
    except KeyError:
        message = {
            'type': 'Failure',
            'failure': 'WrongArguments',
            'message': dict()
        }
        if 'username' not in json:
            message['message']['username'] = 'argument is required'
        if 'password' not in json:
            message['message']['password'] = 'argument is required'
        emit('login', message)
    else:
        found_user = user.get_user(username)
        if not found_user:
            emit('login', {
                'type': 'Failure',
                'failure': 'UserDoesNotExist',
                'message': 'wrong username or password'
            })
        else:
            if not UserModel.verify_hash(password, found_user.password):
                emit('login', {
                    'type': 'Failure',
                    'failure': 'WrongCredentials',
                    'message': 'wrong username or password'
                })
            else:
                login_user(found_user)

                schema = UserSchema()
                result = schema.dump(found_user)

                uts[found_user.username] = request.sid

                emit('login', {
                    'type': 'Success',
                    'message': 'Logged in as {}'.format(found_user.username),
                    'user': result
                })


@sio.on('logout')
def on_logout():
    if current_user.is_authenticated:
        schema = UserSchema()
        result = schema.dump(current_user)

        del uts[current_user.username]

        emit('logout', {
            'type': 'Success',
            'message': 'User {} has been logged out'.format(current_user.username),
            'user': result
        })

        logout_user()
    else:
        emit('logout', {
            'type': 'Failure',
            'failure': 'UserNotAuthenticated',
            'message': 'User is not authenticated'
        })


@sio.on('signup')
def on_signup(json=None):
    if json is None:
        json = dict()
    try:
        username = json['username']
        password = json['password']
        email = json['email']
        created_user = user.create_user(username, password, email)
    except KeyError:
        message = {
            'type': 'Failure',
            'failure': 'WrongArguments',
            'message': dict()
        }
        if 'username' not in json:
            message['message']['username'] = 'argument is required'
        if 'password' not in json:
            message['message']['password'] = 'argument is required'
        if 'email' not in json:
            message['message']['email'] = 'argument is required'
        emit('signup', message)
    except user.UserAlreadyExist:
        emit('signup', {
            'type': 'Failure',
            'failure': 'UserAlreadyExist',
            'message': 'Username {} already exist'.format(json['username'])
        })
    else:
        schema = UserSchema()
        result = schema.dump(created_user)

        emit('signup', {
            'type': 'Success',
            'message': 'Register in as {}'.format(created_user.username),
            'user': result
        })


@sio.on('disconnect')
def on_signup():
    if current_user.is_authenticated:
        del uts[current_user.username]
