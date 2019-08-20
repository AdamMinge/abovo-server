from .base import ResourceDoesNotExist, ResourceAlreadyExist


class UserAlreadyExist(ResourceAlreadyExist):
    pass


class UserDoesNotExist(ResourceDoesNotExist):
    pass

