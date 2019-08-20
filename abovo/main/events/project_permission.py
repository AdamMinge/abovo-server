from flask_socketio import emit
from .. import sio
from ..services import project, project_permission
from ..models import ProjectPermissionTypes
from ..utils.model_schemes import ProjectPermissionSchema
from ..utils.event_decorators import auth


@sio.on('project_permission/get')
@auth.authenticated_only
@auth.check_user_project_permission('project_permission/get', ProjectPermissionTypes.Subscriber)
def on_project_permissions_get(project_id, json=None):
    if json is None:
        json = dict()
    project_permissions_collection = project.get_project_permissions(project_id).all()
    schema = ProjectPermissionSchema(many=True)
    result = schema.dump(project_permissions_collection)

    emit('project_permission/get', {
        'type': 'Success',
        'project_permissions': result
    })


@sio.on('project_permission/add')
@auth.authenticated_only
@auth.check_user_project_permission('project_permission/add', ProjectPermissionTypes.Subscriber)
def on_project_permissions_add(project_id, json=None):
    if json is None:
        json = dict()
    try:
        permission_type = json['type']
        diagram_name = json['username']
        created_project_permission = project_permission.create_project_permission(
            permission_type=ProjectPermissionTypes.from_name(permission_type),
            username=diagram_name,
            project_id=project_id)
    except KeyError:
        message = {
            'type': 'Failure',
            'failure': 'WrongArguments',
            'message': dict()
        }
        if 'name' not in json:
            message['message']['name'] = 'argument is required'
        emit('project_permission/add', message)
    else:
        schema = ProjectPermissionSchema()
        result = schema.dump(created_project_permission)

        emit('project_permission/add', {
            'type': 'Success',
            'project_permission': result
        })


@sio.on('project_permission/get')
def on_project_permission_by_id_get(json=None):
    pass


@sio.on('project_permission/update')
def on_project_permission_by_id_update(json=None):
    pass


@sio.on('project_permission/delete')
def on_project_permission_by_id_delete():
    pass
