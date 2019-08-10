from flask_restful import fields

user_fields = {
    "url": fields.Url(endpoint='user_by_username', absolute=True),
    "username": fields.String,
    "email": fields.String,
    "projects": fields.Url(endpoint='user_projects', absolute=True),
    "tokens": fields.Url(endpoint='user_tokens', absolute=True)
}
