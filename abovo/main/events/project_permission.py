from flask_socketio import emit
from .. import sio
from ..services import project, project_permission
from ..models import ProjectPermissionTypes
from ..utils.model_schemes import ProjectPermissionSchema
from ..utils.event_decorators import auth


@sio.on('project/permissions/get')
@auth.authenticated_only
@auth.check_user_project_permission('project/permissions/get', ProjectPermissionTypes.Subscriber)
def on_project_permissions_get(project_id, json=None):
    if json is None:
        json = dict()
    project_permissions_collection = project.get_project_permissions(project_id).all()
    schema = ProjectPermissionSchema(many=True)
    result = schema.dump(project_permissions_collection)

    emit('project/permissions/get', {
        'type': 'Success',
        'permissions': result
    })


@sio.on('project/permissions/add')
@auth.authenticated_only
@auth.check_user_project_permission('project/permissions/add', ProjectPermissionTypes.Administrator)
def on_project_permissions_add(project_id, json=None):
    if json is None:
        json = dict()
    try:
        permission_type = json['type']
        username = json['username']
        created_project_permission = project_permission.create_project_permission(
            permission_type=ProjectPermissionTypes.from_name(permission_type),
            username=username,
            project_id=project_id)
    except KeyError:
        message = {
            'type': 'Failure',
            'failure': 'WrongArguments',
            'message': dict()
        }
        if 'name' not in json:
            message['message']['name'] = 'argument is required'
        emit('project/permissions/add', message)
    except project_permission.ProjectPermissionAlreadyExist:
        emit('project/permissions/add', {
            'type': 'Failure',
            'failure': 'ProjectPermissionAlreadyExist',
            'message': 'Project permission for user {} and project {} already exist'
             .format(json['username'], project_id)})
    except project_permission.ProjectDoesNotExist:
        emit('project/permissions/add', {
            'type': 'Failure',
            'failure': 'ProjectDoesNotExist',
            'message': 'Project with id {} does mot exist'
             .format(project_id)})
    except project_permission.UserDoesNotExist:
        emit('project/permissions/add', {
            'type': 'Failure',
            'failure': 'UserDoesNotExist',
            'message': 'User with username {} does mot exist'
             .format(json['username'])})
    else:
        schema = ProjectPermissionSchema()
        result = schema.dump(created_project_permission)

        emit('project/permissions/add', {
            'type': 'Success',
            'permission': result
        })


@sio.on('project/permission/get')
@auth.authenticated_only
@auth.check_user_project_permission('project/permission/get', ProjectPermissionTypes.Subscriber)
def on_project_permission_by_id_get(project_permission_id, json=None):
    if json is None:
        json = dict()
    found_project_permission = project_permission.get_project_permission(project_permission_id)
    if not found_project_permission:
        emit('project/permission/get', {
            'type': 'Failure',
            'failure': 'ProjectPermissionDoesNotExist',
            'message': 'project permission with this id does not exist'
        })
    else:
        schema = ProjectPermissionSchema()
        result = schema.dump(found_project_permission)

        emit('project/permission/get', {
            'type': 'Success',
            'permission': result
        })


@sio.on('project/permission/update')
@auth.authenticated_only
@auth.check_user_project_permission('project/permission/update', ProjectPermissionTypes.Administrator)
def on_project_permission_by_id_update(project_permission_id, json=None):
    if json is None:
        json = dict()
    try:
        updated_project_permission = project_permission.update_project_permission(project_permission_id, **json)
    except project_permission.ProjectPermissionDoesNotExist:
        emit('project/permission/update', {
            'type': 'Failure',
            'failure': 'ProjectPermissionDoesNotExist',
            'message': 'project permission with this id does not exist'
        })
    else:
        schema = ProjectPermissionSchema()
        result = schema.dump(updated_project_permission)

        emit('project/permission/update', {
            'type': 'Success',
            'permission': result
        })


@sio.on('project/permission/delete')
@auth.authenticated_only
@auth.check_user_project_permission('project/permission/delete', ProjectPermissionTypes.Administrator)
def on_project_permission_by_id_delete(project_permission_id):
    try:
        found_project_permission = project_permission.get_project_permission(project_permission_id)
        project_permission.delete_project_permission(project_permission_id)
    except project_permission.ProjectPermissionDoesNotExist:
        emit('project/permission/delete', {
            'type': 'Failure',
            'failure': 'ProjectPermissionDoesNotExist',
            'message': 'project permission with this id does not exist'
        })
    else:
        schema = ProjectPermissionSchema()
        result = schema.dump(found_project_permission)

        emit('project/permission/delete', {
            'type': 'Success',
            'permission': result
        })
