from flask_restful import Resource
from flask_jwt_extended import fresh_jwt_required
from utils.decorators import pagination, auth
from utils.model_queries import user
from utils.model_fields import token_fields


class UserTokens(Resource):
    @fresh_jwt_required
    @auth.self_only
    @pagination.marshal_with(token_fields)
    @pagination.paginate()
    def get(self, username):
        return user.get_user_tokens(username)

    @fresh_jwt_required
    @auth.self_only
    @pagination.marshal_with(token_fields)
    @pagination.paginate()
    def delete(self, username):
        user.delete_user_tokens(username)
        return {'message': 'All user tokens has been removed'}
