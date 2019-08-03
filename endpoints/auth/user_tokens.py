from flask_restful import Resource, marshal_with, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.blacklist_helpers import get_user_tokens


token_fields = {
    "id": fields.Integer,
    "jti": fields.String,
    "token_type": fields.String,
    "user_identity": fields.String,
    "revoked": fields.Boolean,
    "expires": fields.DateTime,
}

token_list_fields = {
    "count": fields.Integer,
    "tokens": fields.List(fields.Nested(token_fields))
}


class UserTokens(Resource):
    @jwt_required
    @marshal_with(token_list_fields)
    def get(self):
        user_identity = get_jwt_identity()
        all_tokens = get_user_tokens(user_identity)
        return {"count": len(all_tokens),
                "tokens": all_tokens}
