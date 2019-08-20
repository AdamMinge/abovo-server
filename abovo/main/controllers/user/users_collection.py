from flask_restful import Resource
from flask_jwt_extended import jwt_required
from ..user import user_api
from ...utils.controller_decorators import pagination
from ...utils.model_fields import user_fields
from ...services import user


class UsersCollection(Resource):
    @jwt_required
    @pagination.marshal_with(user_fields)
    @pagination.paginate()
    def get(self):
        return user.get_users()


user_api.add_resource(UsersCollection,
                      '/users',
                      endpoint='users_collection')
