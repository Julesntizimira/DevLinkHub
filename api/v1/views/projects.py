from flask import make_response, jsonify, request, abort
from models.user import User, Profile
from models.project import Project
from models import storage
from . import app_views


@app_views.route('/projects', methods=['GET'], strict_slashes=False)
def projects():
    '''all profiles'''
    projects = [project.to_dict() for project in storage.all(Project).values()]
    return make_response(jsonify(projects), 200)