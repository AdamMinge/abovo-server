from flask_restful import Resource
from flask_jwt_extended import jwt_required
from ..project import project_api
from ...models import ProjectPermissionTypes
from ...utils.controller_decorators import pagination, auth
from ...utils.model_fields import user_fields
from ...services import project


class ProjectUsers(Resource):
    @jwt_required
    @auth.check_user_project_permission(ProjectPermissionTypes.Subscriber)
    @pagination.marshal_with(user_fields)
    @pagination.paginate()
    def get(self, project_id):
        return project.get_project_users(project_id)


project_api.add_resource(ProjectUsers,
                         '/project/<int:project_id>/users',
                         endpoint='project_users')

