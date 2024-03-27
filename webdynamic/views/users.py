from flask import request, abort, render_template, redirect, url_for, flash
from models.user import User, Profile
from models import storage
from . import app_views
from forms.user import UserForm, ProfileForm
from utils.handleImage import handleImage, allowed_file
from utils.handleUserCreation import userAccountCreate, profileAccountUpdate
from flask_login import current_user, login_required
from utils.paginate import paginate
from flask_mail import Message
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()



user_attr = [
        'username',
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
    profiles = []
    searchQuery = None
    if request.args.get('text'):
        searchQuery = request.args.get('text').lower()
        for profile in storage.all(Profile).values():
            if (profile.name and searchQuery in profile.name.lower()) or (profile.bio and searchQuery in profile.bio.lower()):
                    profiles.append(profile)
            else:
                for skill in profile.skills:
                    if searchQuery in skill.name.lower():
                        profiles.append(profile)
                        break
    else:
        profiles = list(storage.all(Profile).values())
    page = int(request.args.get('page', 1))
    # Number of profiles per page
    items_on_page, total_pages, custom_range = paginate(profiles, page)
    context = {
        'items_on_page': items_on_page,
        'total_pages': total_pages,
        'queryPage': page,
        'custom_range': custom_range,
        'searchQuery': searchQuery if searchQuery else None
        }
    return render_template('profiles.html', **context)

@app_views.route('/profile/<profile_id>', methods=['GET'], strict_slashes=False)
def profile(profile_id):
    '''specific profile'''
    profile = storage.get(Profile, profile_id)
    skills = [skill for skill in profile.skills if skill.description ]
    otherSkills = [skill for skill in profile.skills if not skill.description]
    return render_template('profile.html', profile=profile, skills=skills, otherSkills=otherSkills)



@app_views.route('/account', methods=['GET'], strict_slashes=False)
@login_required
def account():
    '''user account'''
    profile = current_user.profile
    print(profile.name)
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
                return render_template('create_update_form.html', form=form)
        if form.profile_image.data:
            img = form.profile_image.data
            if not allowed_file(img.filename):
                flash('image formats accepted: png, jpg, jpeg, gif', 'error')
                return render_template('create_update_form.html', form=form)
        userAccountCreate(form, request)
        return redirect(url_for('app_views.login'))
    return render_template('create_update_form.html', form=form)


@app_views.route('/update_profile', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def update_profile():
    '''update profile'''
    profile = current_user.profile
    form = ProfileForm(obj=profile)
    if request.method == 'POST' and form.validate_on_submit:
        username = form.username.data.lower()
        for prof in storage.all(Profile).values():
            if prof.username == username:
                if prof.id != profile.id:
                    flash('User with the same username already exists', 'error')
                    return render_template('create_update_form.html', form=form)
                break
        if form.profile_image.data:
            img = form.profile_image.data
            if not allowed_file(img.filename):
                flash('image formats accepted: png, jpg, jpeg, gif', 'error')
                return render_template('create_update_form.html', form=form)
        profileAccountUpdate(form, request, profile)
        return redirect(url_for('app_views.account'))
    return render_template('create_update_form.html', form=form)


@app_views.route('/delete_profile', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def delete_profile():
    '''delete user account'''
    if request.method == 'POST':
        current_user.delete()
        return redirect(url_for('app_views.login'))
    return render_template('delete.html')




