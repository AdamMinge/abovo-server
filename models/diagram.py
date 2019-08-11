from app import db


class DiagramModel(db.Model):
    __tablename__ = 'Diagrams'

    diagram_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    creation_time = db.Column(db.DateTime, nullable=False)
    last_edition_time = db.Column(db.DateTime, nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey("Projects.project_id"), nullable=False)

    def __init__(self, name, creation_time, last_edition_time, project_id):
        self.name = name
        self.creation_time = creation_time
        self.last_edition_time = last_edition_time
        self.project_id = project_id

    def __repr__(self):
        return "<Diagram(name='{}', creation_time='{}', last_edition_time='{}', project_id='{}')>" \
            .format(self.name, self.creation_time, self.last_edition_time, self.project_id)
