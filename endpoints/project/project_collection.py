from flask_restful import Resource, marshal_with, reqparse
from models import ProjectPermissionTypes
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.decorators import auth, pagination
from utils.model_fields import project_fields
from utils.model_queries import user, project, project_permission


add_project_perser = reqparse.RequestParser()
add_project_perser.add_argument('name', type=str, help='This field cannot be blank', required=True)


class ProjectsCollection(Resource):
    @jwt_required
    @marshal_with(project_fields)
    def post(self):
        data = add_project_perser.parse_args()
        new_project = project.create_project(data['name'])
        project_permission.create_project_permission(
            permission_type=ProjectPermissionTypes.Administrator,
            username=get_jwt_identity(),
            project_id=new_project.project_id)

    @jwt_required
    @pagination.marshal_with(project_fields)
    @pagination.paginate()
    def get(self):
        return user.get_user_projects(get_jwt_identity())
