import datetime
from ..models import ProjectModel, ProjectPermissionModel, UserModel, DiagramModel
from ..utils.exceptions import ProjectDoesNotExist
from ..models import ProjectPermissionTypes
from ..services import project_permission
from .. import db


def create_project(project_name, username):
    new_project = ProjectModel(
        name=project_name,
        creation_time=datetime.datetime.now(),
        last_edition_time=datetime.datetime.now()
    )
    db.session.add(new_project)
    db.session.commit()
    project_permission.create_project_permission(
        permission_type=ProjectPermissionTypes.Administrator,
        username=username,
        project_id=new_project.project_id)

    return new_project


def get_project(project_id):
    user = ProjectModel.query.filter_by(project_id=project_id).first()
    if not user:
        raise ProjectDoesNotExist
    return user


def get_projects():
    return ProjectModel.query


def update_project(project_id, **kwargs):
    current_project = get_project(project_id)
    if 'name' in kwargs:
        current_project.name = kwargs.get('name')
    db.session.commit()
    return current_project


def delete_project(project_id):
    current_project = ProjectModel.query.filter_by(project_id=project_id).first()
    if not current_project:
        raise ProjectDoesNotExist
    db.session.delete(current_project)
    db.session.commit()


def get_project_permissions(project_id):
    return db.session.query(ProjectPermissionModel) \
        .filter(ProjectPermissionModel.project_id == project_id)


def get_project_users(project_id):
    return db.session.query(ProjectPermissionModel) \
        .join(UserModel) \
        .filter(ProjectPermissionModel.project_id == project_id)


def get_project_diagrams(project_id):
    return db.session.query(DiagramModel) \
        .filter(DiagramModel.project_id == project_id)
