from flask_restful import Resource, reqparse
from models import UserModel
from flask_jwt_extended import create_access_token, create_refresh_token
from utils.blacklist_helpers import add_token_to_database
from app import app


login_perser = reqparse.RequestParser()
login_perser.add_argument('username', help='This field cannot be blank', required=True)
login_perser.add_argument('password', help='This field cannot be blank', required=True)


class UserLogin(Resource):
    def post(self):
        data = login_perser.parse_args()
        current_user = UserModel.find_by_username(data['username'])

        if not current_user:
            return {'message': 'User {} doesn\'t exist'.format(data['username'])}

        if UserModel.verify_hash(data['password'], current_user.password):

            access_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])

            add_token_to_database(access_token, app.config['JWT_IDENTITY_CLAIM'])
            add_token_to_database(refresh_token, app.config['JWT_IDENTITY_CLAIM'])

            return {
                'message': 'Logged in as {}'.format(current_user.username),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        else:
            return {'message': 'Wrong credentials'}
