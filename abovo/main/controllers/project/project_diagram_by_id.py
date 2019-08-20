from flask_restful import Resource, marshal_with, reqparse
from flask_jwt_extended import jwt_required, fresh_jwt_required
from ..project import project_api
from ...models import ProjectPermissionTypes
from ...utils.controller_decorators import auth
from ...utils.model_fields import diagram_fields
from ...services import diagram


update_diagram_perser = reqparse.RequestParser()
update_diagram_perser.add_argument('name', type=str, required=False, store_missing=False)


class ProjectDiagramById(Resource):
    @jwt_required
    @auth.check_user_project_permission(ProjectPermissionTypes.Subscriber)
    @marshal_with(diagram_fields)
    def get(self, project_id, diagram_id):
        return diagram.get_diagram(diagram_id)

    @jwt_required
    @auth.check_user_project_permission(ProjectPermissionTypes.Editor)
    @marshal_with(diagram_fields)
    def put(self, project_id, diagram_id):
        return diagram.update_diagram(diagram_id, **update_diagram_perser.parse_args())

    @fresh_jwt_required
    @auth.check_user_project_permission(ProjectPermissionTypes.Administrator)
    def delete(self, project_id, diagram_id):
        diagram.delete_diagram(diagram_id)
        return {'message': 'Diagram has been removed'}


project_api.add_resource(ProjectDiagramById,
                         '/project/<int:project_id>/diagram/<int:diagram_id>',
                         endpoint='project_diagram_by_id')