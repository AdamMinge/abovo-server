from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token
from utils.model_queries import token_blacklist, user
from app import app


register_perser = reqparse.RequestParser()
register_perser.add_argument('username', type=str, help='This field cannot be blank', required=True)
register_perser.add_argument('password', type=str, help='This field cannot be blank', required=True)
register_perser.add_argument('email', type=str, help='This field cannot be blank', required=True)


class UserRegistration(Resource):
    def post(self):
        data = register_perser.parse_args()
        new_user = user.create_user(username=data['username'],
                                    password=data['password'],
                                    email=data['email'])

        access_token = create_access_token(identity=new_user.username, fresh=True)
        refresh_token = create_refresh_token(identity=new_user.username)
        token_blacklist.add_token_to_database(access_token, app.config['JWT_IDENTITY_CLAIM'])
        token_blacklist.add_token_to_database(refresh_token, app.config['JWT_IDENTITY_CLAIM'])

        return {
            'message': 'Registered as {}'.format(data['username']),
            'access_token': access_token,
            'refresh_token': refresh_token
        }
