from flask_socketio import emit
from .. import sio
from ..services import diagram, project
from ..models import ProjectPermissionTypes
from ..utils.model_schemes import DiagramSchema
from ..utils.event_decorators import auth


@sio.on('project/diagrams/get')
@auth.authenticated_only
@auth.check_user_project_permission('project/diagrams/get', ProjectPermissionTypes.Subscriber)
def on_project_diagrams_get(project_id, json=None):
    if json is None:
        json = dict()
    project_diagrams = project.get_project_diagrams(project_id).all()
    schema = DiagramSchema(many=True)
    result = schema.dump(project_diagrams)

    emit('project/diagrams/get', {
        'type': 'Success',
        'diagrams': result
    })


@sio.on('project/diagrams/add')
@auth.authenticated_only
@auth.check_user_project_permission('project/diagrams/add', ProjectPermissionTypes.Editor)
def on_project_diagrams_add(project_id, json=None):
    if json is None:
        json = dict()
    try:
        diagram_name = json['name']
        created_diagram = diagram.create_diagram(diagram_name, project_id)
    except KeyError:
        message = {
              'type': 'Failure',
              'failure': 'WrongArguments',
              'message': dict()
        }
        if 'name' not in json:
            message['message']['name'] = 'argument is required'
        emit('project/diagrams/add', message)
    else:
        schema = DiagramSchema()
        result = schema.dump(created_diagram)

        emit('project/diagrams/add', {
            'type': 'Success',
            'project': result
        })


@sio.on('project/diagram/get')
@auth.authenticated_only
@auth.check_user_project_permission('project/diagram/get', ProjectPermissionTypes.Subscriber)
def on_project_diagram_by_id_get(diagram_id, json=None):
    if json is None:
        json = dict()
    try:
        found_diagram = diagram.get_diagram(diagram_id)
    except diagram.DiagramDoesNotExist:
        emit('project/diagram/get', {
            'type': 'Failure',
            'failure': 'DiagramDoesNotExist',
            'message': 'diagram with this id does not exist'
        })
    else:
        schema = DiagramSchema()
        result = schema.dump(found_diagram)

        emit('project/diagram/get', {
            'type': 'Success',
            'diagrams': result
        })


@sio.on('project/diagram/update')
@auth.authenticated_only
@auth.check_user_project_permission('project/diagram/update', ProjectPermissionTypes.Editor)
def on_project_diagram_by_id_update(diagram_id, json=None):
    if json is None:
        json = dict()
    try:
        updated_diagram = diagram.update_diagram(diagram_id, **json)
    except diagram.DiagramDoesNotExist:
        emit('project/diagram/update', {
            'type': 'Failure',
            'failure': 'DiagramDoesNotExist',
            'message': 'diagram with this id does not exist'
        })
    else:
        schema = DiagramSchema()
        result = schema.dump(updated_diagram)

        emit('project/diagram/update', {
            'type': 'Success',
            'project': result
        })


@sio.on('project/diagram/delete')
@auth.authenticated_only
@auth.check_user_project_permission('project/diagram/delete', ProjectPermissionTypes.Administrator)
def on_project_diagram_by_id_delete(diagram_id):
    try:
        diagram.delete_diagram(diagram_id)
    except diagram.DiagramDoesNotExist:
        emit('project/diagram/delete', {
            'type': 'Failure',
            'failure': 'DiagramDoesNotExist',
            'message': 'diagram with this id does not exist'
        })
    else:
        emit('project/diagram/delete', {
            'type': 'Success'
        })
