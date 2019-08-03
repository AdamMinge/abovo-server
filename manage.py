import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_restful import Api
from app import app, db, socketio, jwt, login_manager

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    app.config.from_object(os.environ.get('FLASK_ENV') or 'config.DevelopementConfig')
    db.init_app(app)

    api = Api(app)
    db.init_app(app)
    socketio.init_app(app)
    jwt.init_app(app)
    login_manager.init_app(app)

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

    manager.run()
