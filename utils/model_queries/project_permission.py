from models import ProjectPermissionModel
from utils.exceptions import ProjectPermissionNotExist, ProjectDoesNotExist, UserDoesNotExist
from utils.model_queries import project, user
from app import db


def create_project_permission(permission_type, username, project_id):
    project_for_project_permission = project.get_project(project_id)
    user_for_project_permission = user.get_user(username)

    if not project_for_project_permission:
        raise ProjectDoesNotExist

    if not user_for_project_permission:
        raise UserDoesNotExist

    new_project_permission = ProjectPermissionModel(
        type=permission_type,
        username=username,
        project_id=project_id
    )
    db.session.add(new_project_permission)
    db.session.commit()
    return new_project_permission


def get_project_permission(project_permission_id):
    user = ProjectPermissionModel.query.filter_by(project_permission_id=project_permission_id).first()
    if not user:
        raise ProjectPermissionNotExist
    return user


def get_projects_permissions():
    return ProjectPermissionModel.query


def update_project_permission(project_permission_id, **kwargs):
    current_project_permission = get_project_permission(project_permission_id)
    if 'type' in kwargs:
        permission_type = ProjectPermissionModel.ProjectPermissionTypes.from_name(kwargs.get('type'))
        current_project_permission.type = permission_type
    db.session.commit()
    return current_project_permission


def delete_project_permission(project_permission_id):
    current_project_permission = ProjectPermissionModel.query.filter_by(
        project_permission_id=project_permission_id).first()
    if not current_project_permission:
        raise ProjectPermissionNotExist
    db.session.delete(current_project_permission)
    db.session.commit()

