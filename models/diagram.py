from app import db


class DiagramModel(db.Model):
    __tablename__ = 'Diagrams'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    creationTime = db.Column(db.Date)
    lastEditionTime = db.Column(db.Date)
    projectId = db.Column(db.Integer, db.ForeignKey("Projects.id"))

    def __init__(self, name, creationTime, lastEditionTime, projectId):
        self.name = name
        self.creationTime = creationTime
        self.lastEditionTime = lastEditionTime
        self.projectId = projectId

    def __repr__(self):
        return "<Diagram(name='{}', creationTime='{}', lastEditionTime={}, projectId={})>" \
            .format(self.name, self.creationTime, self.lastEditionTime, self.projectId)