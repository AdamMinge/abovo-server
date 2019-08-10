from app import db


class ProjectModel(db.Model):
    __tablename__ = 'Projects'

    project_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    creation_time = db.Column(db.Date, nullable=False)
    last_edition_time = db.Column(db.Date, nullable=False)

    diagrams = db.relationship("DiagramModel")
    project_permissions = db.relationship("ProjectPermissionModel")

    def __init__(self, name, creation_time, last_edition_time):
        self.name = name
        self.creation_time = creation_time
        self.last_edition_time = last_edition_time

    def __repr__(self):
        return "<Project(id='{}', name='{}', creation_time='{}', last_edition_time='{}')>" \
            .format(self.id, self.name, self.creation_time, self.last_edition_time)
