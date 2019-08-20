from .base import AuthenticationError, ResourceDoesNotExist


class TokenDoesNotExist(ResourceDoesNotExist):
    pass


class PermissionDenied(AuthenticationError):
    pass


class WrongCredentials(AuthenticationError):
    pass
