from app import db


class PermissionModel(db.Model):
    __tablename__ = 'Permissions'

    id = db.Column(db.Integer, primary_key=True)
    flag = db.Column(db.Integer)
    userId = db.Column(db.Integer, db.ForeignKey("Users.id"))
    projectId = db.Column(db.Integer, db.ForeignKey("Projects.id"))

    def __init__(self, flag, userId, projectId):
        self.flag = flag
        self.userId = userId
        self.projectId = projectId

    def __repr__(self):
        return "<Permission(id='{}', flag='{}', userId={}, projectId={})>" \
            .format(self.id, self.flag, self.userId, self.projectId)
