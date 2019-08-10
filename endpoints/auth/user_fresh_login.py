from flask_restful import Resource, reqparse
from models import UserModel
from flask_jwt_extended import create_access_token
from utils.model_queries import token_blacklist, user
from app import app


login_perser = reqparse.RequestParser()
login_perser.add_argument('username', type=str, help='This field cannot be blank', required=True)
login_perser.add_argument('password', type=str, help='This field cannot be blank', required=True)


class UserFreshLogin(Resource):
    def post(self):
        data = login_perser.parse_args()
        current_user = user.get_user(data['username'])

        if UserModel.verify_hash(data['password'], current_user.password):

            access_token = create_access_token(identity=current_user.username, fresh=True)
            token_blacklist.add_token_to_database(access_token, app.config['JWT_IDENTITY_CLAIM'])

            return {
                'message': 'Logged in as {}'.format(current_user.username),
                'access_token': access_token
            }
        else:
            return {'message': 'Wrong credentials'}
