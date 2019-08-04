import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from flask_restful import Api


app = Flask(__name__)
app.config.from_object(os.environ.get('FLASK_ENV') or 'config.DevelopementConfig')

api = Api(app)
db = SQLAlchemy(app)
socketio = SocketIO(app)
jwt = JWTManager(app)
login_manager = LoginManager(app)


def add_auth_resources():
    from endpoints import auth
    api.add_resource(auth.UserRegistration, '/registration')
    api.add_resource(auth.UserLogin, '/login')
    api.add_resource(auth.TokenRefresh, '/token/refresh')
    api.add_resource(auth.UserTokens, '/tokens')
    api.add_resource(auth.UserLogoutRefresh, '/logout/refresh')
    api.add_resource(auth.UserLogoutAccess, '/logout/access')


def add_user_resources():
    from endpoints import user
    api.add_resource(user.User, '/user/<string:username>')
    api.add_resource(user.UsersCollection, '/users')


if __name__ == "__main__":
    from utils import is_token_revoked

    @jwt.token_in_blacklist_loader
    def check_if_token_revoked(decoded_token):
        return is_token_revoked(decoded_token)

    add_auth_resources()
    add_user_resources()

    socketio.run(app)
