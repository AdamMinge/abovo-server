from flask_restful import fields


token_fields = {
    "token_id": fields.Integer,
    "jti": fields.String,
    "token_type": fields.String,
    "revoked": fields.Boolean,
    "expires": fields.DateTime,
    "url": fields.Url('user_api.user_token_by_id', absolute=True),
    "user": fields.Url('user_api.user_by_username', absolute=True)
}
