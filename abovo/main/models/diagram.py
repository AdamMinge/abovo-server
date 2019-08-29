from sqlalchemy.ext.hybrid import hybrid_property
from .. import db


class DiagramModel(db.Model):
    __tablename__ = 'Diagrams'

    diagram_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    creation_time = db.Column(db.DateTime, nullable=False)
    last_edition_time = db.Column(db.DateTime, nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey("Projects.project_id"), nullable=False)

    project = db.relationship('ProjectModel', foreign_keys=project_id)

    @hybrid_property
    def display_name(self):
        return self.name + '#{}'.format(self.diagram_id)

    def __init__(self, name, creation_time, last_edition_time, project_id):
        self.name = name
        self.creation_time = creation_time
        self.last_edition_time = last_edition_time
        self.project_id = project_id

    def __repr__(self):
        return "<Diagram(diagram_id='{}' name='{}', creation_time='{}', last_edition_time='{}', project_id='{}')>" \
            .format(self.diagram_id, self.name, self.creation_time, self.last_edition_time, self.project_id)
