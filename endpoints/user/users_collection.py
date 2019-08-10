from flask_restful import Resource
from flask_jwt_extended import jwt_required
from utils.decorators import pagination
from utils.model_fields import user_fields
from utils.model_queries import user


class UsersCollection(Resource):
    @jwt_required
    @pagination.marshal_with(user_fields)
    @pagination.paginate()
    def get(self):
        return user.get_users()
