from flask import make_response, jsonify, request, abort, render_template
from models import storage
from api.v1.views import app_views
from models.project import Tag


@app_views.route('/tags', methods=['GET'], strict_slashes=False)
def get_tags():
    '''all tags'''
    tags = [tag.to_dict() for tag in storage.all(Tag).values()]
    return make_response(jsonify(tags), 200)


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