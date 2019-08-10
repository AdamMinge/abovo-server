from flask_restful import fields


diagram_fields = {
    "url": fields.Url(endpoint='diagram_by_id', absolute=True),
    "diagram_id": fields.Integer,
    "name": fields.String,
    "creation_time": fields.DateTime,
    "last_edition_time": fields.DateTime,
    "project": fields.Url(endpoint='project_by_id', absolute=True)
}
