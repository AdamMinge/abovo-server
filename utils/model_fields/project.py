from flask_restful import fields


project_fields = {
    "project_id": fields.Integer,
    "name": fields.String,
    "creation_time": fields.DateTime,
    "last_edition_time": fields.DateTime,
    "url": fields.Url(endpoint='project_by_id', absolute=True),
    "diagrams": fields.Url(endpoint='project_diagrams', absolute=True),
    "users": fields.Url(endpoint='project_users', absolute=True),
    "permissions": fields.Url(endpoint='project_permissions', absolute=True)
}
