from flask import Blueprint
from flask_restful import Api

user_blueprint = Blueprint('user_api', __name__)
user_api = Api()
user_api.init_app(user_blueprint)

from .user_by_username import UserByUsername
from .user_projects import UserProjects
from .user_token_by_id import UserTokenById
from .user_tokens import UserTokens
from .users_collection import UsersCollection
