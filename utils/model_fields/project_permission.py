from flask_restful import fields


project_permission_fields = {
    "url": fields.Url(endpoint='project_permission_by_id', absolute=True),
    "project_permission_id": fields.Integer,
    "type": fields.String,
    "user": fields.Url(endpoint='user_by_username', absolute=True),
    "project": fields.Url(endpoint='project_by_id', absolute=True)
}
