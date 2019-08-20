from flask_jwt_extended import create_access_token, create_refresh_token
from flask_restful import Resource, reqparse
from ..auth import auth_api
from ...services import token_blacklist, user


register_perser = reqparse.RequestParser()
register_perser.add_argument('username', type=str, help='This field cannot be blank', required=True)
register_perser.add_argument('password', type=str, help='This field cannot be blank', required=True)
register_perser.add_argument('email', type=str, help='This field cannot be blank', required=True)


class UserRegistration(Resource):
    def post(self):
        data = register_perser.parse_args()
        username = data['username']
        password = data['password']
        email = data['email']

        new_user = user.create_user(username=username,
                                    password=password,
                                    email=email)

        access_token = create_access_token(identity=new_user.username, fresh=True)
        refresh_token = create_refresh_token(identity=new_user.username)
        token_blacklist.add_token_to_database(access_token)
        token_blacklist.add_token_to_database(refresh_token)

        return {
            'message': 'Registered as {}'.format(username),
            'access_token': access_token,
            'refresh_token': refresh_token
        }


auth_api.add_resource(UserRegistration,
                      '/registration',
                      endpoint='registration')
