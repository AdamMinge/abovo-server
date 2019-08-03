from flask_restful import Resource
from flask_jwt_extended import create_access_token, jwt_refresh_token_required, get_jwt_identity
from utils.blacklist_helpers import add_token_to_database
from app import app


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        user_identity = get_jwt_identity()
        access_token = create_access_token(identity=user_identity)
        add_token_to_database(access_token, app.config['JWT_IDENTITY_CLAIM'])
        return {'access_token': access_token}
