from flask_restful import Resource, marshal_with, reqparse
from flask_jwt_extended import jwt_required, fresh_jwt_required
from ..project import project_api
from ...models import ProjectPermissionTypes
from ...utils.controller_decorators import auth
from ...utils.model_fields import project_fields
from ...utils.exceptions import ProjectDoesNotExist
from ...services import project


update_project_perser = reqparse.RequestParser()
update_project_perser.add_argument('name', type=str, required=False, store_missing=False)


class ProjectById(Resource):
    @jwt_required
    @auth.check_user_project_permission(ProjectPermissionTypes.Subscriber)
    @marshal_with(project_fields)
    def get(self, project_id):
        found_project = project.get_project(project_id)
        if not found_project:
            raise ProjectDoesNotExist
        return found_project

    @jwt_required
    @auth.check_user_project_permission(ProjectPermissionTypes.Administrator)
    @marshal_with(project_fields)
    def put(self, project_id):
        return project.update_project(project_id, **update_project_perser.parse_args())

    @fresh_jwt_required
    @auth.check_user_project_permission(ProjectPermissionTypes.Administrator)
    def delete(self, project_id):
        project.delete_project(project_id)
        return {'message': 'Project has been removed'}


project_api.add_resource(ProjectById,
                         '/project/<int:project_id>',
                         endpoint='project_by_id')
