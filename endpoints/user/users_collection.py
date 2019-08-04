from flask_restful import Resource, marshal_with, fields
from models import UserModel
from flask_jwt_extended import jwt_required
from utils import paginate, meta_fields


user_fields = {
    "username": fields.String,
    "email": fields.String,
}


users_list_fields = {
    "items": fields.List(fields.Nested(user_fields)),
    'meta': fields.Nested(meta_fields),
}


class UsersCollection(Resource):
    @jwt_required
    @marshal_with(users_list_fields)
    @paginate()
    def get(self):
        return UserModel.find_all()
