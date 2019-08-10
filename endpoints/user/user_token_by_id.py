from flask_restful import Resource, marshal_with
from flask_jwt_extended import fresh_jwt_required
from utils.decorators import auth
from utils.model_queries import user
from utils.model_fields import token_fields


class UserTokenById(Resource):
    @fresh_jwt_required
    @auth.self_only
    @marshal_with(token_fields)
    def get(self, username, token_id):
        return user.get_user_token(username, token_id)

    @fresh_jwt_required
    @auth.self_only
    @marshal_with(token_fields)
    def delete(self, username, token_id):
        user.delete_user_token(username, token_id)
        return {'message': 'Token has been removed'}
