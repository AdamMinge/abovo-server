from flask import Blueprint
from flask_restful import Api

auth_blueprint = Blueprint('auth_api', __name__)
auth_api = Api()
auth_api.init_app(auth_blueprint)

from .token_refresh import TokenRefresh
from .user_fresh_login import UserFreshLogin
from .user_login import UserLogin
from .user_logout_access import UserLogoutAccess
from .user_logout_refresh import UserLogoutRefresh
from .user_registration import UserRegistration
