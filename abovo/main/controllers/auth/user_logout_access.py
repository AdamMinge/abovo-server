from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, get_raw_jwt
from ..auth import auth_api
from ...services import token_blacklist


class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        username = get_jwt_identity()
        token_id = get_raw_jwt()
        return token_blacklist.revoke_token(token_id, username)


auth_api.add_resource(UserLogoutAccess,
                      '/logout/access',
                      endpoint='user_logout_access')