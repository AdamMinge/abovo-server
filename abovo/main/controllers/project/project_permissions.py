from flask_restful import Resource, reqparse, marshal_with
from flask_jwt_extended import jwt_required
from ..project import project_api
from ...models import ProjectPermissionTypes
from ...utils.controller_decorators import pagination, auth
from ...utils.model_fields import project_permission_fields
from ...services import project, project_permission


add_project_permission_perser = reqparse.RequestParser()
add_project_permission_perser.add_argument('type', type=str, required=True,
                                           choices=('Subscriber', 'Editor', 'Administrator'))
add_project_permission_perser.add_argument('username', type=str, required=True)


class ProjectPermissions(Resource):
    @jwt_required
    @auth.check_user_project_permission(ProjectPermissionTypes.Subscriber)
    @pagination.marshal_with(project_permission_fields)
    @pagination.paginate()
    def get(self, project_id):
        return project.get_project_permissions(project_id)

    @jwt_required
    @auth.check_user_project_permission(ProjectPermissionTypes.Administrator)
    @marshal_with(project_permission_fields)
    def post(self, project_id):
        data = add_project_permission_perser.parse_args()
        return project_permission.create_project_permission(
            permission_type=ProjectPermissionTypes.from_name(data['type']),
            username=data['username'],
            project_id=project_id)


project_api.add_resource(ProjectPermissions,
                         '/project/<int:project_id>/permissions',
                         endpoint='project_permissions')
