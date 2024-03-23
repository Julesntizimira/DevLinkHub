from flask import make_response, jsonify, request, abort
from models.user import User, Profile
from models import storage
from . import app_views



# urlpatterns = [
#     path('', views.profiles, name='profiles' ),
#     path('profile/<str:id>/', views.userProfile, name='user-profile'),
#     path('login/', views.loginPage, name='login'),
#     path('logout/', views.logoutUser, name='logout'),
#     path('register/', views.registerUser, name='register'),
#     path('account/', views.userAccount, name='account'),
#     path('edit-account/', views.editAccount, name='edit-account'),
#     path('create-skill/', views.createSkill, name='create-skill'),
#     path('update-skill/<str:id>', views.updateSkill, name='update-skill'),
#     path('delete-skill/<str:id>', views.deleteSkill, name='delete-skill'),
#     path('inbox/', views.inbox, name='inbox'),
#     path('message/<str:id>', views.viewMessage, name='message'),
#     path('create-message/<str:id>', views.createMessage, name='create-message'),
# ]

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