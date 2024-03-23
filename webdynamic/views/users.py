from flask import request, abort, render_template, redirect, url_for, flash
from models.user import User, Profile, Skill
from models import storage
from . import app_views
from forms.user import UserForm, ProfileForm, SkillForm
from utils.handleImage import handleImage



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

user_attr = [
        'username',
        'password',
        'email',
        'name'
        ]

profile_attr = [
    'location',
    'bio',
    'headline',
    'social_github',
    'social_linkdin',
    'social_youtube',
    'social_twitter'
    ]

@app_views.route('/profiles', methods=['GET'], strict_slashes=False)
def profiles():
    '''all profiles'''
    profiles = storage.all(Profile).values()
    return render_template('profiles.html', profiles=profiles)

@app_views.route('/profile/<profile_id>', methods=['GET'], strict_slashes=False)
def profile(profile_id):
    '''specific profile'''
    profile = storage.get(Profile, profile_id)
    skills = [skill for skill in profile.skills if skill.description ]
    otherSkills = [skill for skill in profile.skills if not skill.description]
    return render_template('profile.html', profile=profile, skills=skills, otherSkills=otherSkills)

@app_views.route('/account', methods=['GET'], strict_slashes=False)
def account():
    '''user account'''
    profile = storage.get(Profile, 'f9aa840f-26f4-4ded-8fb3-d1829dd1f356')
    return render_template('account.html', profile=profile)


@app_views.route('/create_profile', methods=['GET', 'POST'], strict_slashes=False)
def create_profile():
    '''create_profile'''
    users = storage.all(User).values()
    form = UserForm()
    if request.method == 'POST' and form.validate_on_submit:
        username = form.username.data.lower()
        for user in users:
            if user.username == username:
                flash('User with the same username already exists', 'error')
                return redirect(url_for('app_views.profiles'))
        data = { k: v for k, v in request.form.items() if k in user_attr}
        new_user = User(**data)
        new_user.username = username
        new_user.save()
        profile = new_user.profile
        if form.profile_image.data:
            profile.profile_image_url = handleImage(form.profile_image.data, profile.id, 'profile')
            profile.save()
        return redirect(url_for('app_views.profiles'))
    return render_template('create_update_form.html', form=form)

@app_views.route('/update_profile/<profile_id>', methods=['GET', 'POST'], strict_slashes=False)
def update_profile(profile_id):
    '''update profile'''
    profile = storage.get(Profile, profile_id)
    form = ProfileForm(obj=profile)
    if request.method == 'POST' and form.validate_on_submit:
        username = form.username.data.lower()
        for prof in storage.all(Profile).values():
            if prof.username == username:
                if prof.id != profile.id:
                    flash('User with the same username already exists', 'error')
                    return redirect(url_for('app_views.profiles'))
        user_data = { k: v for k, v in request.form.items() if k in user_attr}
        user = profile.user
        for attr, val in user_data.items():
            setattr(user, attr, val)
        user.save()
        profile_data = { k: v for k, v in request.form.items() if k in profile_attr}
        for attr, val in profile_data.items():
            setattr(profile, attr, val)
        if form.profile_image.data:
            profile.profile_image_url = handleImage(form.profile_image.data, profile.id, 'profile')
        profile.save()
        return redirect(url_for('app_views.profiles'))
    return render_template('create_update_form.html', form=form)


@app_views.route('/delete_profile/<profile_id>', methods=['GET', 'POST'], strict_slashes=False)
def delete_profile(profile_id):
    '''delete project'''
    profile = storage.get(Profile, profile_id)
    if request.method == 'POST':
        form = request.form
    return render_template('delete.html')




