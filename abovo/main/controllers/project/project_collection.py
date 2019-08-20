from flask_restful import Resource, marshal_with, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..project import project_api
from ...utils.controller_decorators import pagination
from ...utils.model_fields import project_fields
from ...services import project, user


add_project_perser = reqparse.RequestParser()
add_project_perser.add_argument('name', type=str, help='This field cannot be blank', required=True)


class ProjectsCollection(Resource):
    @jwt_required
    @marshal_with(project_fields)
    def post(self):
        data = add_project_perser.parse_args()
        return project.create_project(data['name'], get_jwt_identity())

    @jwt_required
    @pagination.marshal_with(project_fields)
    @pagination.paginate()
    def get(self):
        return user.get_user_projects(get_jwt_identity())


project_api.add_resource(ProjectsCollection,
                         '/projects',
                         endpoint='projects_collection')