from marshmallow import Schema, fields


class DiagramSchema(Schema):
    diagram_id = fields.Integer()
    name = fields.String()
    creation_time = fields.DateTime()
    last_edition_time = fields.DateTime()
    project_id = fields.Integer()
