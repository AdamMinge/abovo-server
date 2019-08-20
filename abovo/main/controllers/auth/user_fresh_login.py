from flask_jwt_extended import create_access_token
from flask_restful import Resource, reqparse
from ..auth import auth_api
from ...models import UserModel
from ...services import token_blacklist, user
from ...utils.exceptions import WrongCredentials


login_perser = reqparse.RequestParser()
login_perser.add_argument('username', type=str, help='This field cannot be blank', required=True)
login_perser.add_argument('password', type=str, help='This field cannot be blank', required=True)


class UserFreshLogin(Resource):
    def post(self):
        data = login_perser.parse_args()
        username = data['username']
        password = data['password']

        current_user = user.get_user(username)

        if not UserModel.verify_hash(password, current_user.password):
            raise WrongCredentials

        access_token = create_access_token(identity=current_user.username, fresh=True)
        token_blacklist.add_token_to_database(access_token)

        return {
            'message': 'Logged in as {}'.format(current_user.username),
            'access_token': access_token
        }


auth_api.add_resource(UserFreshLogin,
                      '/fresh-login',
                      endpoint='fresh-login')
