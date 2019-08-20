import functools
from flask_login import current_user
from flask_socketio import disconnect, emit
from ...services import user


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


def check_user_project_permission(message, min_permission):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            have_permission = user.user_have_permission_for_project(
                username=current_user.username,
                project_id=kwargs['project_id'],
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
