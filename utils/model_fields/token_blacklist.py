from flask_restful import fields


token_fields = {
    "url": fields.Url('user_token_by_id', absolute=True),
    "token_id": fields.Integer,
    "jti": fields.String,
    "token_type": fields.String,
    "revoked": fields.Boolean,
    "expires": fields.DateTime,
    "user": fields.Url('user_by_username', absolute=True)
}
