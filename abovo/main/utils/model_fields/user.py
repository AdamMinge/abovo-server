from flask_restful import fields


user_fields = {
    "username": fields.String,
    "email": fields.String,
    "url": fields.Url(endpoint='user_api.user_by_username', absolute=True),
    "projects": fields.Url(endpoint='user_api.user_projects', absolute=True),
    "tokens": fields.Url(endpoint='user_api.user_tokens', absolute=True)
}
