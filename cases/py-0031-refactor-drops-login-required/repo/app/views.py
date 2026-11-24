from app.auth import login_required
from app.store import store


@login_required
def list_projects(request):
    user = request.user
    result = store.projects_for(user.id)
    return {'projects': result}


@login_required
def get_project(request, project_id):
    user = request.user
    result = store.project(user.id, project_id)
    return {'project': result}


@login_required
def create_project(request):
    user = request.user
    body = request.json
    result = store.create_project(user.id, body)
    return {'project': result}


@login_required
def rename_project(request, project_id):
    user = request.user
    body = request.json
    result = store.rename_project(user.id, project_id, body['name'])
    return {'project': result}


@login_required
def archive_project(request, project_id):
    user = request.user
    result = store.archive_project(user.id, project_id)
    return {'project': result}


@login_required
def list_members(request, project_id):
    user = request.user
    result = store.members(user.id, project_id)
    return {'members': result}


@login_required
def invite_member(request, project_id):
    user = request.user
    body = request.json
    result = store.invite(user.id, project_id, body['email'])
    return {'invite': result}


@login_required
def remove_member(request, project_id):
    user = request.user
    body = request.json
    result = store.remove_member(user.id, project_id, body['user_id'])
    return {'member': result}


@login_required
def export_project(request, project_id):
    user = request.user
    result = store.export(user.id, project_id)
    return {'export': result}


@login_required
def delete_project(request, project_id):
    user = request.user
    result = store.delete_project(project_id)
    return {'deleted': result}


@login_required
def update_profile(request):
    user = request.user
    body = request.json
    result = store.update_profile(user.id, body)
    return {'profile': result}


@login_required
def list_api_keys(request):
    user = request.user
    result = store.api_keys(user.id)
    return {'keys': result}
