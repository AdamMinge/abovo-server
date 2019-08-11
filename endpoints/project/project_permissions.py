from flask_restful import Resource
from models import ProjectPermissionModel
from flask_jwt_extended import jwt_required
from utils.decorators import pagination, auth
from utils.model_queries import project
from utils.model_fields import project_permission_fields


class ProjectPermissions(Resource):
    @jwt_required
    @auth.check_user_project_permission(ProjectPermissionModel.ProjectPermissionTypes.Subscriber)
    @pagination.marshal_with(project_permission_fields)
    @pagination.paginate()
    def get(self, project_id):
        return project.get_project_permissions(project_id)

