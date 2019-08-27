from sqlalchemy import event
from flask_socketio import emit
from ..models import ProjectModel, DiagramModel, ProjectPermissionModel
from ..utils.model_schemes import ProjectSchema, DiagramSchema, ProjectPermissionSchema
from .. import uts


@event.listens_for(ProjectModel, 'after_update')
def project_update_listener(mapper, connection, target):
    schema = ProjectSchema()
    result = schema.dump(target)
    emit('listener/project/updated', {
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

    if target.username in uts:
        emit('listener/project/permission/inserted', {
            'project_id': target.project_id,
            'permission': result
        }, room=uts[target.username])


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
