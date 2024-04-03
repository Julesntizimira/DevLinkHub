from flask import make_response, jsonify, request, abort
from models.user import User, Profile
from models import storage
from . import app_views

@app_views.route('/profiles', methods=['GET'], strict_slashes=False)
def get_profiles():
    '''all profiles'''
    profiles = [profile.to_dict() for profile in storage.all(Profile).values()]
    return make_response(jsonify(profiles), 200)

@app_views.route('/profile/<id>', methods=['GET'], strict_slashes=False)
def get_profile(id):
    '''specific profile'''
    profile = storage.get(profile, str(id))
    return make_response(jsonify(profile.to_dict()), 200)

@app_views.route('/profile', methods=['POST'], strict_slashes=False)
def post_profile():
    '''specific profile'''
    data = request.get_json()
    users = [user.to_dict() for user in storage.all(User).values()]
    if not data.get('email'):
        abort(400, 'Email is Missing')
    if not data.get('password'):
        abort(400, 'password is Missing')
    if not data.get('username'):
        abort(400, 'username is Missing')
    if not data.get('first_name'):
        abort(400, 'first_name is Missing')
    if not data.get('last_name'):
        abort(400, 'last name is Missing')
    for user in users:
        if user.get('username') == data.get('username'):
            abort(409, 'User with the same username already exist')
    new_user = User(**data)
    new_user.save()
    return make_response(jsonify(new_user.profile.to_dict()), 201)