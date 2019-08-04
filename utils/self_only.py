import functools
from flask_jwt_extended import get_jwt_identity


def self_only(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        user_identity = get_jwt_identity()
        if user_identity != kwargs['username']:
            return {'message': 'Permission denied'}
        return func(*args, **kwargs)
    return wrapper
