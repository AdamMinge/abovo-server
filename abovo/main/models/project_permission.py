from .. import db
from ..utils.enums import OrderedEnum


class ProjectPermissionTypes(OrderedEnum):
    Subscriber = 1
    Editor = 2
    Administrator = 3

    @classmethod
    def permission_greater_or_equal(cls, permission):
        ans = []
        for name, member in cls.__members__.items():
            if member >= permission:
                ans.append(member)
        return ans

    @classmethod
    def from_name(cls, permission_name):
        for name, member in cls.__members__.items():
            if name == permission_name:
                return member
        raise ValueError('{} is not a valid project permission name'.format(permission_name))


class ProjectPermissionModel(db.Model):
    __tablename__ = 'ProjectPermissions'

    project_permission_id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Enum(ProjectPermissionTypes), nullable=False)
    username = db.Column(db.String, db.ForeignKey("Users.username"), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey("Projects.project_id"), nullable=False)

    def __init__(self, type, username, project_id):
        self.type = type
        self.username = username
        self.project_id = project_id
        self.type = type

    def __repr__(self):
        return "<ProjectPermission(project_permission_id='{}', type='{}', username='{}', project_id='{}')>" \
            .format(self.project_permission_id, self.type, self.username, self.project_id)
