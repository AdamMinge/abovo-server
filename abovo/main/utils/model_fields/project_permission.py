from flask_restful import fields
from .fields.enum import Enum


project_permission_fields = {
    "project_permission_id": fields.Integer,
    "type": Enum(),
    "url": fields.Url(endpoint='project_api.project_permission_by_id', absolute=True),
    "user": fields.Url(endpoint='user_api.user_by_username', absolute=True),
    "project": fields.Url(endpoint='project_api.project_by_id', absolute=True)
}
