from flask import make_response, jsonify, request, abort
from models.user import User, Profile
from models.project import Project
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

@app_views.route('/projects', methods=['GET'], strict_slashes=False)
def projects():
    '''all profiles'''
    projects = [project.to_dict() for project in storage.all(Project).values()]
    return make_response(jsonify(projects), 200)