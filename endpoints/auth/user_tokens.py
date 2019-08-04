from flask_restful import Resource, marshal_with, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import TokenBlacklistModel
from utils import paginate, meta_fields


token_fields = {
    "id": fields.Integer,
    "jti": fields.String,
    "token_type": fields.String,
    "user_identity": fields.String,
    "revoked": fields.Boolean,
    "expires": fields.DateTime,
}

token_list_fields = {
    "items": fields.List(fields.Nested(token_fields)),
    'meta': fields.Nested(meta_fields),
}


class UserTokens(Resource):
    @jwt_required
    @marshal_with(token_list_fields)
    @paginate()
    def get(self):
        user_identity = get_jwt_identity()
        all_tokens = TokenBlacklistModel.query.filter_by(user_identity=user_identity)
        return all_tokens
