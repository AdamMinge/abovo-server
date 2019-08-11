from flask_restful import Resource, marshal_with, reqparse
from models import ProjectPermissionTypes
from flask_jwt_extended import jwt_required, fresh_jwt_required
from utils.decorators import auth
from utils.model_fields import diagram_fields
from utils.model_queries import diagram


update_diagram_perser = reqparse.RequestParser()
update_diagram_perser.add_argument('name', type=str, required=False, store_missing=False)


class ProjectDiagramById(Resource):
    @jwt_required
    @auth.check_user_project_permission(ProjectPermissionTypes.Subscriber)
    @marshal_with(diagram_fields)
    def get(self, diagram_id):
        return diagram.get_diagram(diagram_id)

    @jwt_required
    @auth.check_user_project_permission(ProjectPermissionTypes.Editor)
    @marshal_with(diagram_fields)
    def put(self, diagram_id):
        return diagram.update_diagram(diagram_id, **update_diagram_perser.parse_args())

    @fresh_jwt_required
    @auth.check_user_project_permission(ProjectPermissionTypes.Administrator)
    def delete(self, diagram_id):
        diagram.delete_diagram(diagram_id)
        return {'message': 'Diagram has been removed'}
