import functools
from flask_login import current_user
from flask_socketio import disconnect, emit
from ...services import user, diagram, project_permission


def self_only(message):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            user_identity = current_user.username
            if user_identity != kwargs['username']:
                emit(message, {
                    'type': 'Failure',
                    'failure': 'PermissionDenied',
                    'message': 'Not permission to this user'
                })
            return func(*args, **kwargs)

        return wrapper

    return decorator


def _get_project_id(**kwargs):
    project_id = None
    if 'project_id' in kwargs:
        project_id = kwargs['project_id']
    else:
        if 'diagram_id' in kwargs:
            try:
                project_id = diagram.get_diagram(kwargs['diagram_id']).project_id
            except diagram.DiagramDoesNotExist:
                project_id = None
        elif 'project_permission_id' in kwargs:
            try:
                project_id = project_permission.get_project_permission(kwargs['project_permission_id']).project_id
            except project_permission.ProjectPermissionDoesNotExist:
                project_id = None
    return project_id


def check_user_project_permission(message, min_permission):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            project_id = _get_project_id(**kwargs)

            if not project_id:
                emit(message, {
                    'type': 'Failure',
                    'failure': 'ProjectDoesNotExist',
                    'message': 'project with this id does not exist'
                })
                return

            have_permission = user.user_have_permission_for_project(
                username=current_user.username,
                project_id=project_id,
                min_permission=min_permission)

            if not have_permission:
                emit(message, {
                    'type': 'Failure',
                    'failure': 'PermissionDenied',
                    'message': 'Not permission to this project'
                })
            else:
                return func(*args, **kwargs)
        return wrapper
    return decorator


def authenticated_only(func):
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            disconnect()
        else:
            return func(*args, **kwargs)
    return wrapped
