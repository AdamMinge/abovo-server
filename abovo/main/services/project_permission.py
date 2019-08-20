from ..models import ProjectPermissionModel
from ..utils.exceptions import (ProjectPermissionDoesNotExist, ProjectDoesNotExist,
                                UserDoesNotExist, ProjectPermissionAlreadyExist)
from ..services import project, user
from .. import db


def create_project_permission(permission_type, username, project_id):
    project_for_project_permission = project.get_project(project_id)
    user_for_project_permission = user.get_user(username)
    permission_already_exist = user.user_have_permission_for_project(username, project_id)

    if not project_for_project_permission:
        raise ProjectDoesNotExist

    if not user_for_project_permission:
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
    if not current_user:
        raise ProjectPermissionDoesNotExist
    return current_user


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
        raise ProjectPermissionDoesNotExist
    db.session.delete(current_project_permission)
    db.session.commit()
