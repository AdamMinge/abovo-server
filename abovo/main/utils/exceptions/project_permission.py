from .base import ResourceDoesNotExist, ResourceAlreadyExist


class ProjectPermissionDoesNotExist(ResourceDoesNotExist):
    pass


class ProjectPermissionAlreadyExist(ResourceAlreadyExist):
    pass
