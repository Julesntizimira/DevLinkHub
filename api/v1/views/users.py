'''users and profile routes'''
from flask import make_response, jsonify, request, abort
from models.user import User, Profile
from models import storage
from . import app_views
from utils.paginate import apiPagination
from flask_bcrypt import Bcrypt
from utils.handleProjectSearch import profile_search
import os

bcrypt = Bcrypt()

user_attr = [
        'username',
        'email',
        'name'
        ]

profile_attr = [
    'name',
    'location',
    'bio',
    'headline',
    'social_github',
    'social_linkdin',
    'social_youtube',
    'social_twitter'
    ]


if os.getenv('DOMAIN_NAME'):
    domain = os.getenv('DOMAIN_NAME')
else:
    domain = 'http://127.0.0.1:5100'


@app_views.route('/profiles', methods=['GET'], strict_slashes=False)
def get_profiles():
    '''all profiles'''
    profiles = [ {'title': profile.name, 'id': profile.id, 'link': f'{domain}/api/v1/profile/{profile.id}'} for profile in storage.all(Profile).values()]
    result = apiPagination(profiles, request)
    return make_response(jsonify(result), 200)

@app_views.route('/profiles/search', methods=['GET'], strict_slashes=False)
def search_profiles():
    '''search profiles'''
    searchQuery = request.args.get('searchQuery')
    if searchQuery:
        queryProfiles = profile_search(searchQuery)
        profiles = [ {'title': profile.name, 'id': profile.id, 'link': f'{domain}/api/v1/profile/{profile.id}'} for profile in queryProfiles]
        result = apiPagination(profiles, request)
    else:
        result = {}
    return make_response(jsonify(result), 200)

    

@app_views.route('/profile/<id>', methods=['GET'], strict_slashes=False)
def get_profile(id):
    '''specific profile'''
    profile = storage.get(Profile, id)
    return make_response(jsonify(profile.to_dict()), 200)

@app_views.route('/profile', methods=['POST'], strict_slashes=False)
def create_profile():
    '''specific profile'''
    data = request.get_json()
    users = [user.to_dict() for user in storage.all(User).values()]
    if not data.get('email'):
        abort(400, 'Email is Missing')
    if not data.get('password'):
        abort(400, 'password is Missing')
    if not data.get('username'):
        abort(400, 'username is Missing')
    if not data.get('name'):
        abort(400, 'name is Missing')
    for user in users:
        if user.get('username') == data.get('username'):
            abort(409, 'User with the same username already exist')
    hashed_password = bcrypt.generate_password_hash(data.get('password'))
    data_checked = { k: v for k, v in request.form.items() if k in user_attr}
    data_checked['password'] = hashed_password
    new_user = User(**data_checked)
    new_user.save()
    return make_response(jsonify(new_user.profile.to_dict()), 201)

@app_views.route('/profile/<id>', methods=['PUT'], strict_slashes=False)
def post_profile(id):
    '''Update specific profile'''
    profile = storage.get(profile, str(id))
    if not profile:
        abort(400, 'profile does not exist')
    user = profile.user
    data = request.get_json()
    user_data = { k: v for k, v in data.items() if k in user_attr}
    for attr, val in user_data.items():
        setattr(user, attr, val)
    user.save()
    profile_data = { k: v for k, v in data.items() if k in profile_attr}
    for attr, val in profile_data.items():
        setattr(profile, attr, val)
    profile.save()
    return make_response(jsonify(profile.to_dict()), 201)

@app_views.route('/profile/<id>', methods=['DELETE'], strict_slashes=False)
def delete_profile(id):
    '''delete specific profile'''
    profile = storage.get(profile, str(id))
    if not profile:
        abort(400, 'profile does not exist')
    user = profile.user
    user.delete()
    return make_response(jsonify({}), 201)