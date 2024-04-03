'''project api views'''
from flask import make_response, jsonify, request, abort
from models.user import User, Profile
from models.project import Project
from models import storage
from utils.paginate import apiPagination
from utils.handleProjectSearch import project_search
from . import app_views
import os


if os.getenv('DOMAIN_NAME'):
    domain = os.getenv('DOMAIN_NAME')
else:
    domain = 'http://127.0.0.1:5100'


@app_views.route('/projects', methods=['GET'], strict_slashes=False)
def projects():
    '''all projects'''
    projects = [ {'title': project.title, 'id': project.id, 'link': f'{domain}/api/v1/project/{project.id}'} for project in storage.all(Project).values()]
    result = apiPagination(projects, request)
    return make_response(jsonify(result), 200)


@app_views.route('/project/<id>', methods=['GET'], strict_slashes=False)
def get_project(id):
    '''specific project'''
    project = storage.get(Project, id)
    project_dict = project.to_dict()
    project_dict['links'] = []
    project_dict['tags'] = []
    for link in project.links:
        project_dict['links'].append({'name': link.name, 'url': link.url})
    for tag in project.tags:
        project_dict['tags'].append({'name': tag.name, 'tag-link': f'{domain}/api/v1/tag/{tag.id}'})
        project_dict['Go back to home'] = f'{domain}/api/v1'
    return make_response(jsonify(project_dict), 200)


@app_views.route('/projects/search', methods=['GET'], strict_slashes=False)
def search_projects():
    '''search projects'''
    searchQuery = request.args.get('searchQuery')
    if searchQuery:
        queryProjects = project_search(searchQuery)
        projects = [ {'title': project.title, 'id': project.id, 'link': f'{domain}/api/v1/project/{project.id}'} for project in queryProjects]
        result = apiPagination(projects, request)
    else:
        result = {}
    return make_response(jsonify(result), 200)
