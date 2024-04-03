'''home view'''
from flask import make_response, jsonify
from api.v1.views import app_views
import os

@app_views.route('/', methods=['GET'], strict_slashes=False)
def home():
    '''home view'''
    if os.getenv('DOMAIN_NAME'):
        domain = os.getenv('DOMAIN_NAME')
    else:
        domain = 'http://127.0.0.1:5100'
    result = [
        'Welcome to DevLinkHub Api',
        'the dictionary below shows you major Api routes',
        {
            'Get all projects paginated': f'{domain}/api/v1/projects?page=1',
            'Get all userProfiles paginated': f'{domain}/api/v1/profiles?page=1',
            'Get all tags paginated': f'{domain}/api/v1/tags?page=1',
            'Search project by title, tags, links, keywords': f'{domain}/api/v1/projects/search?searchQuery=python'
        }
    ]
    return make_response(jsonify(result), 200)
