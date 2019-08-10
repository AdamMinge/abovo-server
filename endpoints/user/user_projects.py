from flask_restful import Resource
from flask_jwt_extended import jwt_required
from utils.decorators import pagination, auth
from utils.model_queries import user
from utils.model_fields import project_fields


class UserProjects(Resource):
    @jwt_required
    @auth.self_only
    @pagination.marshal_with(project_fields)
    @pagination.paginate()
    def get(self, username):
        return user.get_user_projects(username)
