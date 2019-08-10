from flask_restful import Resource, reqparse, marshal_with
from flask_jwt_extended import jwt_required, fresh_jwt_required
from utils.decorators import auth
from utils.model_queries import user
from utils.model_fields import user_fields


update_user_perser = reqparse.RequestParser()
update_user_perser.add_argument('password', type=str, required=False, store_missing=False)
update_user_perser.add_argument('email', type=str, required=False, store_missing=False)


class UserByUsername(Resource):
    @fresh_jwt_required
    @auth.self_only
    @marshal_with(user_fields)
    def put(self, username):
        return user.update_user(username, **update_user_perser.parse_args())

    @jwt_required
    @marshal_with(user_fields)
    def get(self, username):
        return user.get_user(username)
