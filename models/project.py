from app import db


class ProjectModel(db.Model):
    __tablename__ = 'Projects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    creationTime = db.Column(db.Date)
    lastEditionTime = db.Column(db.Date)

    diagrams = db.relationship("DiagramModel")
    permissions = db.relationship("PermissionModel")

    def __init__(self, login, creationTime, lastEditionTime):
        self.login = login
        self.creationTime = creationTime
        self.lastEditionTime = lastEditionTime

    def __repr__(self):
        return "<Project(id='{}', name='{}', creationTime={}, lastEditionTime={})>" \
            .format(self.id, self.name, self.creationTime, self.lastEditionTime)
