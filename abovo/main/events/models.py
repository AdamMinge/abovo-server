from sqlalchemy import event
from flask_socketio import emit, rooms
from ..models import UserModel, ProjectModel, DiagramModel, ProjectPermissionModel
from ..utils.model_schemes import UserSchema, ProjectSchema, DiagramSchema, ProjectPermissionSchema


@event.listens_for(UserModel, 'after_insert')
def user_append_listener(mapper, connection, target):
    schema = UserSchema()
    result = schema.dump(target)
    open_rooms = rooms()
    for permission in target.permissions:
        if 'project#{}'.format(permission.project_id) in open_rooms:
            emit('listener/user/inserted', {
                'project_id': permission.project_id,
                'user': result
            })


@event.listens_for(UserModel, 'after_update')
def user_update_listener(mapper, connection, target):
    schema = UserSchema()
    result = schema.dump(target)
    open_rooms = rooms()
    for permission in target.permissions:
        if 'project#{}'.format(permission.project_id) in open_rooms:
            emit('listener/user/updated', {
                'project_id': permission.project_id,
                'user': result
            })


@event.listens_for(UserModel, 'after_delete')
def user_delete_listener(mapper, connection, target):
    schema = UserSchema()
    result = schema.dump(target)
    open_rooms = rooms()
    for permission in target.permissions:
        if 'project#{}'.format(permission.project_id) in open_rooms:
            emit('listener/user/deleted', {
                'project_id': permission.project_id,
                'user': result
            })


@event.listens_for(ProjectModel, 'after_insert')
def project_append_listener(mapper, connection, target):
    schema = ProjectSchema()
    result = schema.dump(target)
    emit('listener/project/inserted', {
        'project_id': target.project_id,
        'project': result
    }, room='project#{}'.format(target.project_id))


@event.listens_for(ProjectModel, 'after_update')
def project_update_listener(mapper, connection, target):
    schema = ProjectSchema()
    result = schema.dump(target)
    emit('listener/project/updated', {
        'project_id': target.project_id,
        'project': result
    }, room='project#{}'.format(target.project_id))


@event.listens_for(ProjectModel, 'after_delete')
def project_delete_listener(mapper, connection, target):
    schema = ProjectSchema()
    result = schema.dump(target)
    emit('listener/project/deleted', {
        'project_id': target.project_id,
        'project': result
    }, room='project#{}'.format(target.project_id))


@event.listens_for(DiagramModel, 'after_insert')
def diagram_append_listener(mapper, connection, target):
    schema = DiagramSchema()
    result = schema.dump(target)
    emit('listener/project/diagram/inserted', {
        'project_id': target.project_id,
        'diagram': result
    }, room='project#{}'.format(target.project_id))


@event.listens_for(DiagramModel, 'after_update')
def diagram_update_listener(mapper, connection, target):
    schema = DiagramSchema()
    result = schema.dump(target)
    emit('listener/project/diagram/updated', {
        'project_id': target.project_id,
        'diagram': result
    }, room='project#{}'.format(target.project_id))


@event.listens_for(DiagramModel, 'after_delete')
def diagram_delete_listener(mapper, connection, target):
    schema = DiagramSchema()
    result = schema.dump(target)
    emit('listener/project/diagram/deleted', {
        'project_id': target.project_id,
        'diagram': result
    }, room='project#{}'.format(target.project_id))


@event.listens_for(ProjectPermissionModel, 'after_insert')
def project_permission_append_listener(mapper, connection, target):
    schema = ProjectPermissionSchema()
    result = schema.dump(target)
    emit('listener/project/permission/inserted', {
        'project_id': target.project_id,
        'permission': result
    }, room='project#{}'.format(target.project_id))


@event.listens_for(ProjectPermissionModel, 'after_update')
def project_permission_update_listener(mapper, connection, target):
    schema = ProjectPermissionSchema()
    result = schema.dump(target)
    emit('listener/project/permission/updated', {
        'project_id': target.project_id,
        'permission': result
    }, room='project#{}'.format(target.project_id))


@event.listens_for(ProjectPermissionModel, 'after_delete')
def project_permission_delete_listener(mapper, connection, target):
    schema = ProjectPermissionSchema()
    result = schema.dump(target)
    emit('listener/project/permission/deleted', {
        'project_id': target.project_id,
        'permission': result
    }, room='project#{}'.format(target.project_id))
