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
    'ProjectPermissionNotExist': {
        'message': "A project permission with that id does not exists.",
        'status': 404,
    },
    'ProjectPermissionAlreadyExist': {
        'message': "A project permission for this user and project already exists.",
        'status': 409,
    },
    'ProjectDoesNotExist': {
        'message': "A project with that id does not exists.",
        'status': 404,
    },
    'DiagramDoesNotExist': {
        'message': "A diagram with that id does not exists.",
        'status': 404,
    }
}
