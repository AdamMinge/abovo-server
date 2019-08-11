import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from flask_restful import Api
from errors import errors


app = Flask(__name__)
app.config.from_object(os.environ.get('FLASK_ENV') or 'config.ProductionConfig')


api = Api(app, errors=errors)
db = SQLAlchemy(app)
socketio = SocketIO(app)
jwt = JWTManager(app)
login_manager = LoginManager(app)


def add_auth_resources():
    from endpoints import auth
    api.add_resource(auth.UserRegistration, '/registration',
                     endpoint='registration')
    api.add_resource(auth.UserLogin, '/login',
                     endpoint='login')
    api.add_resource(auth.UserFreshLogin, '/fresh-login',
                     endpoint='fresh-login')
    api.add_resource(auth.TokenRefresh, '/token/refresh',
                     endpoint='token_refresh')
    api.add_resource(auth.UserLogoutRefresh, '/logout/refresh',
                     endpoint='user_logout_refresh')
    api.add_resource(auth.UserLogoutAccess, '/logout/access',
                     endpoint='user_logout_access')


def add_user_resources():
    from endpoints import user
    api.add_resource(user.UserByUsername, '/user/<string:username>',
                     endpoint='user_by_username')
    api.add_resource(user.UserTokens, '/user/<string:username>/tokens',
                     endpoint='user_tokens')
    api.add_resource(user.UserTokenById, '/user/<string:username>/token/<int:token_id>',
                     endpoint='user_token_by_id')
    api.add_resource(user.UsersCollection, '/users',
                     endpoint='users_collection')
    api.add_resource(user.UserProjects, '/user/<string:username>/projects',
                     endpoint='user_projects')


def add_project_resources():
    from endpoints import project
    api.add_resource(project.ProjectById, '/project/<int:project_id>',
                     endpoint='project_by_id')
    api.add_resource(project.ProjectsCollection, '/projects',
                     endpoint='projects_collection')
    api.add_resource(project.ProjectUsers, '/project/<int:project_id>/users',
                     endpoint='project_users')
    api.add_resource(project.ProjectDiagrams, '/project/<int:project_id>/diagrams',
                     endpoint='project_diagrams')
    api.add_resource(project.ProjectDiagramById, '/project/<int:project_id>/diagram/<int:diagram_id>',
                     endpoint='project_diagram_by_id')
    api.add_resource(project.ProjectPermissions, '/project/<int:project_id>/permissions',
                     endpoint='project_permissions')
    api.add_resource(project.ProjectPermissionById, '/project/<int:project_id>/permission/<int:project_permission_id>',
                     endpoint='project_permission_by_id')


if __name__ == "__main__":
    from utils.model_queries import token_blacklist

    @jwt.token_in_blacklist_loader
    def check_if_token_revoked(decoded_token):
        return token_blacklist.is_token_revoked(decoded_token)

    add_auth_resources()
    add_user_resources()
    add_project_resources()

    socketio.run(app)
