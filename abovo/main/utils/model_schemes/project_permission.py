from marshmallow import Schema, fields
from .fields.enum import Enum


class ProjectPermissionSchema(Schema):
    project_permission_id = fields.Integer()
    type = Enum()
    username = fields.String()
    project_id = fields.Integer()
