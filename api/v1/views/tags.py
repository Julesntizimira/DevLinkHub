'''tag api views'''
from flask import make_response, jsonify, request, abort, render_template
from models import storage
from api.v1.views import app_views
from models.project import Tag
from utils.paginate import apiPagination
import os


if os.getenv('DOMAIN_NAME'):
    domain = os.getenv('DOMAIN_NAME')
else:
    domain = 'http://127.0.0.1:5100'


@app_views.route('/tags', methods=['GET'], strict_slashes=False)
def get_tags():
    '''all tags'''
    tags = [{'id': tag.id, 'name': tag.name, 'link to projects in this tag': f'{domain}/api/v1/tag/{tag.id}'} for tag in storage.all(Tag).values()]
    result = apiPagination(tags, request)
    return make_response(jsonify(result), 200)


@app_views.route('/tag/<id>', methods=['GET'], strict_slashes=False)
def get_projects_related_to_tag(id):
    '''get projects in specific tag'''
    tag = storage.get(Tag, id)
    projects = [ {'title': project.title, 'id': project.id, 'link': f'{domain}/api/v1/project/{project.id}'} for project in tag.projects]
    result = apiPagination(projects, request)
    return make_response(jsonify(result), 200)


@app_views.route('/tag', methods=['POST'], strict_slashes=False)
def create_tag():
    '''all tags'''
    tags = [tag.to_dict() for tag in storage.all(Tag).values()]
    data = request.get_json()
    if not data.get('name'):
        abort(400, 'Tag name missing')
    for tag in tags:
        if tag.get('name') == data.get('name'):
            abort(409, 'tag with same name already exists')
    tag = Tag(name=data.get('name'))
    tag.save()
    return make_response(jsonify(tag.to_dict()), 200)