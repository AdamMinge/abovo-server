from flask_restful import Resource
from flask_jwt_extended import create_access_token, jwt_refresh_token_required, get_jwt_identity
from utils.model_queries import token_blacklist
from app import app


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        username = get_jwt_identity()
        access_token = create_access_token(identity=username, fresh=False)
        token_blacklist.add_token_to_database(access_token, app.config['JWT_IDENTITY_CLAIM'])
        return {'access_token': access_token}
