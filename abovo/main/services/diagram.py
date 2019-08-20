from datetime import datetime
from ..models import DiagramModel
from ..utils.exceptions import DiagramDoesNotExist, ProjectDoesNotExist
from ..services import project
from .. import db


def create_diagram(diagram_name, project_id):
    project_for_diagram = project.get_project(project_id)
    if not project_for_diagram:
        raise ProjectDoesNotExist

    new_diagram = DiagramModel(
        name=diagram_name,
        creation_time=datetime.now(),
        last_edition_time=datetime.now(),
        project_id=project_id
    )
    db.session.add(new_diagram)
    db.session.commit()
    return new_diagram


def get_diagram(diagram_id):
    user = DiagramModel.query.filter_by(diagram_id=diagram_id).first()
    if not user:
        raise DiagramDoesNotExist
    return user


def get_diagrams():
    return DiagramModel.query


def update_diagram(diagram_id, **kwargs):
    current_diagram = get_diagram(diagram_id)
    if 'name' in kwargs:
        current_diagram.name = kwargs.get('name')
    db.session.commit()
    return current_diagram


def delete_diagram(diagram_id):
    current_diagram = DiagramModel.query.filter_by(diagram_id=diagram_id).first()
    if not current_diagram:
        raise DiagramDoesNotExist
    db.session.delete(current_diagram)
    db.session.commit()
