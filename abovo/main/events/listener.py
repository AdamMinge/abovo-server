from flask_socketio import join_room, leave_room
from ..models import ProjectPermissionTypes
from ..utils.event_decorators import auth
from .. import sio


@sio.on('listener/project/enable')
@auth.authenticated_only
@auth.check_user_project_permission('project/get', ProjectPermissionTypes.Subscriber)
def on_listener_user_enable(project_id):
    join_room('project#{}'.format(project_id))


@sio.on('listener/project/disable')
@auth.authenticated_only
@auth.check_user_project_permission('project/get', ProjectPermissionTypes.Subscriber)
def on_listener_user_enable(project_id):
    leave_room('project#{}'.format(project_id))
