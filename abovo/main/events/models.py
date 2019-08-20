from sqlalchemy import event
from ..models import UserModel, ProjectModel, DiagramModel, ProjectPermissionModel
from .. import sio


@event.listens_for(UserModel, 'after_insert')
def user_append_listener(target, value, initiator):
    pass


@event.listens_for(UserModel, 'after_update')
def user_update_listener(target, value, initiator):
    pass


@event.listens_for(UserModel, 'after_delete')
def user_delete_listener(target, value, initiator):
    pass


@event.listens_for(ProjectModel, 'after_insert')
def project_append_listener(target, value, initiator):
    pass


@event.listens_for(ProjectModel, 'after_update')
def project_update_listener(target, value, initiator):
    pass


@event.listens_for(ProjectModel, 'after_delete')
def project_delete_listener(target, value, initiator):
    pass


@event.listens_for(DiagramModel, 'after_insert')
def diagram_append_listener(target, value, initiator):
    pass


@event.listens_for(DiagramModel, 'after_update')
def diagram_update_listener(target, value, initiator):
    pass


@event.listens_for(DiagramModel, 'after_delete')
def diagram_delete_listener(target, value, initiator):
    pass


@event.listens_for(ProjectPermissionModel, 'after_insert')
def project_permission_append_listener(target, value, initiator):
    pass


@event.listens_for(ProjectPermissionModel, 'after_update')
def project_permission_update_listener(target, value, initiator):
    pass


@event.listens_for(ProjectPermissionModel, 'after_delete')
def project_permission_delete_listener(target, value, initiator):
    pass
