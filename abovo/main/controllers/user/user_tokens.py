from flask_restful import Resource
from flask_jwt_extended import fresh_jwt_required
from ..user import user_api
from ...utils.controller_decorators import pagination, auth
from ...utils.model_fields import token_fields
from ...services import user


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


user_api.add_resource(UserTokens,
                      '/user/<string:username>/tokens',
                      endpoint='user_tokens')
