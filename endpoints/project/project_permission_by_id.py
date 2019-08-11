from flask_restful import Resource, marshal_with, reqparse
from models import ProjectPermissionTypes
from flask_jwt_extended import jwt_required, fresh_jwt_required
from utils.decorators import auth
from utils.model_fields import project_permission_fields
from utils.model_queries import project_permission


update_project_permission_perser = reqparse.RequestParser()
update_project_permission_perser.add_argument('type', type=str, required=False,
                                              store_missing=False, choices=('Subscriber', 'Editor', 'Administrator'))


class ProjectPermissionById(Resource):
    @jwt_required
    @auth.check_user_project_permission(ProjectPermissionTypes.Subscriber)
    @marshal_with(project_permission_fields)
    def get(self, project_permission_id):
        return project_permission.get_project_permission(project_permission_id)

    @jwt_required
    @auth.check_user_project_permission(ProjectPermissionTypes.Administrator)
    @marshal_with(project_permission_fields)
    def put(self, project_permission_id):
        return project_permission.update_project_permission(project_permission_id,
                                                            **update_project_permission_perser.parse_args())

    @fresh_jwt_required
    @auth.check_user_project_permission(ProjectPermissionTypes.Administrator)
    def delete(self, project_permission_id):
        project_permission.delete_project_permission(project_permission_id)
        return {'message': 'User has been removed from project'}
