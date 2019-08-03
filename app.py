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


if __name__ == "__main__":
    from utils.blacklist_helpers import is_token_revoked

    @jwt.token_in_blacklist_loader
    def check_if_token_revoked(decoded_token):
        return is_token_revoked(decoded_token)

    from endpoints.auth import *

    api.add_resource(UserRegistration, '/registration')
    api.add_resource(UserLogin, '/login')
    api.add_resource(TokenRefresh, '/token/refresh')
    api.add_resource(UserTokens, '/token')
    api.add_resource(UserLogoutRefresh, '/logout/refresh')
    api.add_resource(UserLogoutAccess, '/logout/access')

    socketio.run(app)
