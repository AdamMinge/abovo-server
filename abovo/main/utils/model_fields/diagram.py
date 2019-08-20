from flask_restful import fields


diagram_fields = {
    "diagram_id": fields.Integer,
    "name": fields.String,
    "creation_time": fields.DateTime,
    "last_edition_time": fields.DateTime,
    "url": fields.Url(endpoint='project_api.project_diagram_by_id', absolute=True),
    "project": fields.Url(endpoint='project_api.project_by_id', absolute=True)
}
