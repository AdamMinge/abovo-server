errors = {
    'UserAlreadyExist': {
        'message': "A user with that username already exists.",
        'status': 409,
    },
    'UserDoesNotExist': {
        'message': "A user with that username does not exists.",
        'status': 404,
    },
    'TokenDoesNotExist': {
        'message': "A token with that jti does not exists.",
        'status': 404,
    },
    'ExpiredSignatureError': {
        'message': "A token with that jti has expired.",
        'status': 401,
    },
    'PermissionDenied': {
        'message': "Permission denied.",
        'status': 403,
    },
}
