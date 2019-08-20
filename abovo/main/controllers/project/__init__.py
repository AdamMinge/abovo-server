from flask import Blueprint
from flask_restful import Api

project_blueprint = Blueprint('project_api', __name__)
project_api = Api()
project_api.init_app(project_blueprint)

from .project_by_id import ProjectById
from .project_collection import ProjectsCollection
from .project_diagram_by_id import ProjectDiagramById
from .project_permission_by_id import ProjectPermissionById
from .project_permissions import ProjectPermissions
from .project_users import ProjectUsers
from .projects_diagrams import ProjectDiagrams
