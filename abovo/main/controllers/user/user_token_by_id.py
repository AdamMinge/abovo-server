from flask_restful import Resource, marshal_with
from flask_jwt_extended import fresh_jwt_required
from ..user import user_api
from ...utils.controller_decorators import auth
from ...utils.model_fields import token_fields
from ...services import user


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


user_api.add_resource(UserTokenById,
                      '/user/<string:username>/token/<int:token_id>',
                      endpoint='user_token_by_id')
