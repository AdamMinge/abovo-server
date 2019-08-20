from flask_restful import Resource, reqparse, marshal_with
from flask_jwt_extended import jwt_required
from ..project import project_api
from ...models import ProjectPermissionTypes
from ...utils.controller_decorators import pagination, auth
from ...utils.model_fields import diagram_fields
from ...services import project, diagram


add_diagram_perser = reqparse.RequestParser()
add_diagram_perser.add_argument('name', type=str, required=True)


class ProjectDiagrams(Resource):
    @jwt_required
    @auth.check_user_project_permission(ProjectPermissionTypes.Subscriber)
    @pagination.marshal_with(diagram_fields)
    @pagination.paginate()
    def get(self, project_id):
        return project.get_project_diagrams(project_id)

    @jwt_required
    @auth.check_user_project_permission(ProjectPermissionTypes.Editor)
    @marshal_with(diagram_fields)
    def post(self, project_id):
        data = add_diagram_perser.parse_args()
        return diagram.create_diagram(
            diagram_name=data['name'],
            project_id=project_id)


project_api.add_resource(ProjectDiagrams,
                         '/project/<int:project_id>/diagrams',
                         endpoint='project_diagrams')
