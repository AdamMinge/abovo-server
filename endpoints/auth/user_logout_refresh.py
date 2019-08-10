from flask_restful import Resource
from flask_jwt_extended import jwt_refresh_token_required, get_jwt_identity, get_raw_jwt
from utils.model_queries import token_blacklist


class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        username = get_jwt_identity()
        token_id = get_raw_jwt()
        token_blacklist.revoke_token(token_id, username)
        return {'message': 'Refresh token has been revoked'}

