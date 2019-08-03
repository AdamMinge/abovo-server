from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, get_raw_jwt
from utils.blacklist_helpers import revoke_token


class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        user_identity = get_jwt_identity()
        token_id = get_raw_jwt()['jti']
        revoke_token(token_id, user_identity)
        return {'message': 'Access token has been revoked'}
