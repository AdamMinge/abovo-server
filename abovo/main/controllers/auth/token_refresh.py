from flask_jwt_extended import create_access_token
from flask_restful import Resource
from flask_jwt_extended import jwt_refresh_token_required, get_jwt_identity
from ..auth import auth_api
from ...services import token_blacklist


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity, fresh=False)
        token_blacklist.add_token_to_database(access_token)
        return {'access_token': access_token}


auth_api.add_resource(TokenRefresh,
                      '/token/refresh',
                      endpoint='token_refresh')

