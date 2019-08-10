import functools
from flask_jwt_extended import get_jwt_identity
from utils.exceptions import auth
from utils.model_queries import user


def self_only(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        user_identity = get_jwt_identity()
        if user_identity != kwargs['username']:
            raise auth.PermissionDenied()
        return func(*args, **kwargs)
    return wrapper


def check_user_project_permission(min_permission):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            have_permission = user.user_have_permission_for_project(
                username=get_jwt_identity(),
                project_id=kwargs['project_id'],
                min_permission=min_permission)

            if not have_permission:
                raise auth.PermissionDenied()

            return func(*args, **kwargs)
        return wrapper
    return decorator
