from flask_restful import Resource, marshal_with, reqparse
from models import ProjectPermissionModel
from flask_jwt_extended import jwt_required, fresh_jwt_required
from utils.decorators import auth
from utils.model_fields import project_fields
from utils.model_queries import project


update_project_perser = reqparse.RequestParser()
update_project_perser.add_argument('name', type=str, required=False, store_missing=False)


class ProjectById(Resource):
    @jwt_required
    @auth.check_user_project_permission(ProjectPermissionModel.ProjectPermissionTypes.Subscriber)
    @marshal_with(project_fields)
    def get(self, project_id):
        return project.get_project(project_id)

    @jwt_required
    @auth.check_user_project_permission(ProjectPermissionModel.ProjectPermissionTypes.Administrator)
    @marshal_with(project_fields)
    def put(self, project_id):
        return project.update_project(project_id, **update_project_perser.parse_args())

    @fresh_jwt_required
    @auth.check_user_project_permission(ProjectPermissionModel.ProjectPermissionTypes.Administrator)
    def delete(self, project_id):
        project.delete_project(project_id)
        return {'message': 'Project has been removed'}
