from flask import Flask
from flask_session import SqlAlchemySessionInterface
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from .config import config_by_name


# create all application modules
db = SQLAlchemy()
sio = SocketIO(manage_session=True)
jwt = JWTManager()
login_manager = LoginManager()

# map username to sid
uts = {}


def create_app(config_name):
    # initialize application
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    # initialized all application modules
    db.init_app(app)
    sio.init_app(app)
    jwt.init_app(app)
    login_manager.init_app(app)

    # import controllers
    from .controllers.auth import auth_blueprint
    from .controllers.user import user_blueprint
    from .controllers.project import project_blueprint

    # register controllers blueprint
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(project_blueprint)

    # import socket io events
    from .events import (auth, project, user,
                         project_permission, models, diagram)

    # set jwt function which check that token is revoked
    from .services import token_blacklist
    @jwt.token_in_blacklist_loader
    def check_if_token_revoked(decoded_token):
        return token_blacklist.is_token_revoked(decoded_token)

    # set login manager function which load current user from models
    from .services import user
    @login_manager.user_loader
    def load_user(username):
        return user.get_user(username)

    # set sql alchemy session interface
    SqlAlchemySessionInterface(app, db, "sessions", "sess_")

    return app
