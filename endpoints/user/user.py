from flask_restful import Resource, reqparse, marshal_with, fields
from models import UserModel
from flask_jwt_extended import jwt_required
from utils import self_only
from app import db


user_fields = {
    "username": fields.String,
    "email": fields.String,
}


update_user_perser = reqparse.RequestParser()
update_user_perser.add_argument('username', type=str, required=False, store_missing=False)
update_user_perser.add_argument('password', type=str, required=False, store_missing=False)
update_user_perser.add_argument('email', type=str, required=False, store_missing=False)


class User(Resource):
    @jwt_required
    @self_only
    @marshal_with(user_fields)
    def put(self, username):
        data = update_user_perser.parse_args()
        user = UserModel.query.filter_by(username=username).first()

        if not user:
            return {'message': 'User {} doesn\'t exist'.format(username)}

        if 'username' in data:
            user.username = data['username']
        if 'password' in data:
            user.password = UserModel.generate_hash(data.get('password'))
        if 'email' in data:
            user.email = data['email']

        db.session.commit()
        return user

    @jwt_required
    @marshal_with(user_fields)
    def get(self, username):
        user = UserModel.query.filter_by(username=username).first()
        if not user:
            return {'message': 'User {} doesn\'t exist'.format(username)}
        return user
