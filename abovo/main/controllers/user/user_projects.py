from flask_restful import Resource
from flask_jwt_extended import jwt_required
from ..user import user_api
from ...utils.controller_decorators import pagination, auth
from ...utils.model_fields import project_fields
from ...services import user


class UserProjects(Resource):
    @jwt_required
    @auth.self_only
    @pagination.marshal_with(project_fields)
    @pagination.paginate()
    def get(self, username):
        return user.get_user_projects(username)


user_api.add_resource(UserProjects,
                      '/user/<string:username>/projects',
                      endpoint='user_projects')
