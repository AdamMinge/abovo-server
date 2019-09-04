from ..models import ProjectPermissionModel, ProjectModel, UserModel, ProjectPermissionTypes
from ..utils.exceptions import (ProjectPermissionDoesNotExist, ProjectDoesNotExist,
                                UserDoesNotExist, ProjectPermissionAlreadyExist)
from .. import db


def create_project_permission(permission_type, username, project_id):
    found_project = ProjectModel.query.filter_by(project_id=project_id).first()
    found_user = UserModel.query.filter_by(username=username).first()
    permission_already_exist = db.session.query(ProjectPermissionModel).filter(
        ProjectPermissionModel.project_id == project_id,
        ProjectPermissionModel.username == username).count() > 0

    if not found_project:
        raise ProjectDoesNotExist

    if not found_user:
        raise UserDoesNotExist

    if permission_already_exist:
        raise ProjectPermissionAlreadyExist

    new_project_permission = ProjectPermissionModel(
        type=permission_type,
        username=username,
        project_id=project_id
    )
    db.session.add(new_project_permission)
    db.session.commit()
    return new_project_permission


def get_project_permission(project_permission_id):
    current_user = ProjectPermissionModel.query.filter_by(project_permission_id=project_permission_id).first()
    return current_user


def get_projects_permissions():
    return ProjectPermissionModel.query


def update_project_permission(project_permission_id, **kwargs):
    current_project_permission = get_project_permission(project_permission_id)
    if not current_project_permission:
        raise ProjectPermissionDoesNotExist
    if 'type' in kwargs:
        permission_type = ProjectPermissionTypes.from_name(kwargs.get('type'))
        current_project_permission.type = permission_type
    db.session.commit()
    return current_project_permission


def delete_project_permission(project_permission_id):
    current_project_permission = ProjectPermissionModel.query.filter_by(
        project_permission_id=project_permission_id).first()
    if not current_project_permission:
        raise ProjectPermissionDoesNotExist
    db.session.delete(current_project_permission)
    db.session.commit()
