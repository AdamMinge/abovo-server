from flask_restful import Resource, reqparse
from models.user import UserModel
from flask_jwt_extended import create_access_token, create_refresh_token
from utils import add_token_to_database
from app import app, db


register_perser = reqparse.RequestParser()
register_perser.add_argument('username', type=str, help='This field cannot be blank', required=True)
register_perser.add_argument('password', type=str, help='This field cannot be blank', required=True)
register_perser.add_argument('email', type=str, help='This field cannot be blank', required=True)


class UserRegistration(Resource):
    def post(self):
        data = register_perser.parse_args()

        if UserModel.query.filter_by(data['username']).first():
            return {'message': 'User {} already exists'.format(data['username'])}

        new_user = UserModel(
            username=data['username'],
            password=UserModel.generate_hash(data['password']),
            email=data['email']
        )

        db.session.add(new_user)
        db.session.commit()

        access_token = create_access_token(identity=data['username'])
        refresh_token = create_refresh_token(identity=data['username'])
        add_token_to_database(access_token, app.config['JWT_IDENTITY_CLAIM'])
        add_token_to_database(refresh_token, app.config['JWT_IDENTITY_CLAIM'])

        return {
            'message': 'Registered as {}'.format(data['username']),
            'access_token': access_token,
            'refresh_token': refresh_token
        }
