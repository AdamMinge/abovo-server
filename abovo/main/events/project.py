from flask_socketio import emit
from flask_login import current_user
from .. import sio
from ..services import user, project
from ..models import ProjectPermissionTypes
from ..utils.model_schemes import ProjectSchema
from ..utils.event_decorators import auth


@sio.on('projects/get')
@auth.authenticated_only
def on_project_collection_get(json=None):
    if json is None:
        json = dict()
    user_projects = user.get_user_projects(current_user.username).all()
    schema = ProjectSchema(many=True)
    result = schema.dump(user_projects)

    emit('projects/get', {
        'type': 'Success',
        'projects': result
    })


@sio.on('projects/add')
@auth.authenticated_only
def on_project_collection_add(json=None):
    if json is None:
        json = dict()

    try:
        project_name = json['name']
        created_project = project.create_project(project_name, current_user.username)
    except KeyError:
        message = {
            'type': 'Failure',
            'failure': 'WrongArguments',
            'message': dict()
        }
        if 'name' not in json:
            message['message']['name'] = 'argument is required'
        emit('projects/add', message)
    else:
        schema = ProjectSchema()
        result = schema.dump(created_project)

        emit('projects/add', {
            'type': 'Success',
            'project': result
        })


@sio.on('project/get')
@auth.authenticated_only
@auth.check_user_project_permission('project/get', ProjectPermissionTypes.Subscriber)
def on_project_by_id_get(project_id, json=None):
    if json is None:
        json = dict()
    found_project = project.get_project(project_id)
    if not found_project:
        emit('project/get', {
            'type': 'Failure',
            'failure': 'ProjectDoesNotExist',
            'message': 'project with this id does not exist'
        })
    else:
        schema = ProjectSchema()
        result = schema.dump(found_project)

        emit('project/get', {
            'type': 'Success',
            'project': result
        })


@sio.on('project/update')
@auth.authenticated_only
@auth.check_user_project_permission('project/update', ProjectPermissionTypes.Administrator)
def on_project_by_id_update(project_id, json=None):
    if json is None:
        json = dict()
    try:
        updated_project = project.update_project(project_id, **json)
    except project.ProjectDoesNotExist:
        emit('project/update', {
            'type': 'Failure',
            'failure': 'ProjectDoesNotExist',
            'message': 'project with this id does not exist'
        })
    else:
        schema = ProjectSchema()
        result = schema.dump(updated_project)

        emit('project/update', {
            'type': 'Success',
            'project': result
        })


@sio.on('project/delete')
@auth.authenticated_only
@auth.check_user_project_permission('project/delete', ProjectPermissionTypes.Administrator)
def on_project_by_id_delete(project_id):
    try:
        found_project = project.get_project(project_id)
        project.delete_project(project_id)
    except project.ProjectDoesNotExist:
        emit('project/delete', {
            'type': 'Failure',
            'failure': 'ProjectDoesNotExist',
            'message': 'project with this id does not exist'
        })
    else:
        schema = ProjectSchema()
        result = schema.dump(found_project)

        emit('project/delete', {
            'type': 'Success',
            'project': result
        })
