from ..models import UserModel, ProjectModel, ProjectPermissionModel, TokenBlacklistModel, ProjectPermissionTypes
from ..utils.exceptions import UserAlreadyExist, UserDoesNotExist, TokenDoesNotExist
from .. import db


def create_user(username, password, email):
    user = UserModel.query.filter_by(username=username).first()
    if user:
        raise UserAlreadyExist
    new_user = UserModel(
        username=username,
        password=UserModel.generate_hash(password),
        email=email
    )
    db.session.add(new_user)
    db.session.commit()
    return new_user


def get_user(username):
    user = UserModel.query.filter_by(username=username).first()
    return user


def get_users():
    return UserModel.query


def update_user(username, **kwargs):
    current_user = get_user(username)
    if not current_user:
        raise UserDoesNotExist
    if 'password' in kwargs:
        current_user.password = UserModel.generate_hash(kwargs.get('password'))
    if 'email' in kwargs:
        current_user.email = kwargs['email']
    db.session.commit()
    return current_user


def delete_user(username):
    current_user = TokenBlacklistModel.query.filter_by(username=username).first()
    if not current_user:
        raise UserDoesNotExist
    ProjectPermissionModel.query.filter(username=username).delete()
    db.session.delete(current_user)
    db.session.commit()


def get_user_projects(username):
    return db.session.query(ProjectModel)\
                .join(ProjectPermissionModel)\
                .join(UserModel)\
                .filter(UserModel.username == username)


def user_have_permission_for_project(username, project_id, min_permission=None):
    if min_permission:
        return db.session.query(ProjectPermissionModel) \
                    .filter(ProjectPermissionModel.project_id == project_id,
                            ProjectPermissionModel.username == username,
                            ProjectPermissionModel.type.in_(
                                ProjectPermissionTypes.permissions_greater_or_equal(min_permission))).count() > 0
    else:
        return db.session.query(ProjectPermissionModel) \
                   .filter(ProjectPermissionModel.project_id == project_id,
                           ProjectPermissionModel.username == username).count() > 0


def get_user_projects_permissions(username):
    return db.session.query(ProjectPermissionModel) \
                .join(UserModel) \
                .filter(UserModel.username == username)


def get_user_tokens(username):
    return TokenBlacklistModel.query.filter_by(username=username)


def get_user_token(username, token_id):
    token = TokenBlacklistModel.query.filter_by(username=username, token_id=token_id).first()
    return token


def delete_user_token(username, token_id):
    token = TokenBlacklistModel.query.filter_by(username=username, token_id=token_id).first()
    if not token:
        raise TokenDoesNotExist
    db.session.delete(token)
    db.session.commit()


def delete_user_tokens(username):
    TokenBlacklistModel.query().filter_by(username=username).delete()
