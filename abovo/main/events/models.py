from sqlalchemy import event
from flask_socketio import emit,  join_room, leave_room
from ..models import ProjectModel, DiagramModel, ProjectPermissionModel
from ..utils.model_schemes import ProjectSchema, DiagramSchema, ProjectPermissionSchema
from ..services import project
from .. import uts


@event.listens_for(ProjectModel, 'after_update')
def project_update_listener(mapper, connection, target):
    schema = ProjectSchema()
    result = schema.dump(target)
    emit('listener/project/updated', {
        'project': result
    }, room='project#{}'.format(target.project_id))


@event.listens_for(DiagramModel, 'after_insert')
def diagram_append_listener(mapper, connection, target):
    schema = DiagramSchema()
    result = schema.dump(target)
    emit('listener/project/diagram/inserted', {
        'diagram': result
    }, room='project#{}'.format(target.project_id))


@event.listens_for(DiagramModel, 'after_update')
def diagram_update_listener(mapper, connection, target):
    schema = DiagramSchema()
    result = schema.dump(target)
    emit('listener/project/diagram/updated', {
        'diagram': result
    }, room='project#{}'.format(target.project_id))


@event.listens_for(DiagramModel, 'after_delete')
def diagram_delete_listener(mapper, connection, target):
    schema = DiagramSchema()
    result = schema.dump(target)
    emit('listener/project/diagram/deleted', {
        'diagram': result
    }, room='project#{}'.format(target.project_id))


@event.listens_for(ProjectPermissionModel, 'after_insert')
def project_permission_append_listener(mapper, connection, target):
    project_permission_schema = ProjectPermissionSchema()
    project_permission_result = project_permission_schema.dump(target)

    join_room('project#{}'.format(target.project_id), sid=uts[target.username])

    emit('listener/project/permission/inserted', {
        'permission': project_permission_result
    }, room='project#{}'.format(target.project_id))

    if target.username in uts:
        added_project = project.get_project(target.project_id)
        project_schema = ProjectSchema()
        project_result = project_schema.dump(added_project)

        emit('listener/project/inserted', {
            'project': project_result
        }, room=uts[target.username])


@event.listens_for(ProjectPermissionModel, 'after_update')
def project_permission_update_listener(mapper, connection, target):
    schema = ProjectPermissionSchema()
    result = schema.dump(target)
    emit('listener/project/permission/updated', {
        'permission': result
    }, room='project#{}'.format(target.project_id))


@event.listens_for(ProjectPermissionModel, 'after_delete')
def project_permission_delete_listener(mapper, connection, target):
    schema = ProjectPermissionSchema()
    result = schema.dump(target)

    leave_room('project#{}'.format(target.project_id), sid=uts[target.username])

    emit('listener/project/permission/deleted', {
        'permission': result
    }, room='project#{}'.format(target.project_id))

    if target.username in uts:
        added_project = project.get_project(target.project_id)
        project_schema = ProjectSchema()
        project_result = project_schema.dump(added_project)

        emit('listener/project/deleted', {
            'project': project_result
        }, room=uts[target.username])
