from marshmallow import Schema, fields


class TokenBlacklistSchema(Schema):
    token_id = fields.Integer()
    jti = fields.String()
    token_type = fields.String()
    username = fields.String()
    revoked = fields.Bool()
    expires = fields.DateTime()
