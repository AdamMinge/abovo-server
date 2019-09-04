import functools
import inspect
from flask_login import current_user
from flask_socketio import disconnect, emit
from ...services import user, diagram, project_permission


def _get_project_id(**kwargs):
    try:
        project_id = None
        if 'project_id' in kwargs:
            project_id = int(kwargs['project_id'])
        else:
            if 'diagram_id' in kwargs:
                project_id = diagram.get_diagram(int(kwargs['diagram_id'])).project_id
            elif 'project_permission_id' in kwargs:
                project_id = project_permission.get_project_permission(
                    int(kwargs['project_permission_id'])).project_id
    except (TypeError, diagram.DiagramDoesNotExist,
            project_permission.ProjectPermissionDoesNotExist):
        return None
    else:
        return project_id


def self_only(message):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            user_identity = current_user.username
            if user_identity != args[0]:
                emit(message, {
                    'type': 'Failure',
                    'failure': 'PermissionDenied',
                    'message': 'Not permission to this user'
                })
            return func(*args, **kwargs)

        return wrapper

    return decorator


def check_user_project_permission(message, min_permission):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            args_name = list(inspect.signature(func).parameters.keys())
            project_id = _get_project_id(**{args_name[0]: args[0]})

            if project_id is None:
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
