from sqlalchemy.ext.hybrid import hybrid_property
from .. import db


class ProjectModel(db.Model):
    __tablename__ = 'Projects'

    project_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    creation_time = db.Column(db.DateTime, nullable=False)
    last_edition_time = db.Column(db.DateTime, nullable=False)

    diagrams = db.relationship("DiagramModel", backref='project')
    project_permissions = db.relationship("ProjectPermissionModel", backref='project')

    @hybrid_property
    def display_name(self):
        return self.name + '#{}'.format(self.project_id)

    def __init__(self, name, creation_time, last_edition_time):
        self.name = name
        self.creation_time = creation_time
        self.last_edition_time = last_edition_time

    def __repr__(self):
        return "<Project(project_id='{}', name='{}', creation_time='{}', last_edition_time='{}')>" \
            .format(self.project_id, self.name, self.creation_time, self.last_edition_time)
