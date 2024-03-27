'''handle user creation'''
from flask import render_template
from models.user import User
from flask_mail import Message
from .handleImage import handleImage
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


def userAccountCreate(form, request):
    '''User Account creation'''
    username = form.username.data.lower()
    hashed_password = bcrypt.generate_password_hash(form.password.data)
    data = { k: v for k, v in request.form.items() if k in user_attr}
    data['password'] = hashed_password
    new_user = User(**data)
    new_user.username = username
    new_user.save()
    profile = new_user.profile
    if form.profile_image.data:
        profile.profile_image_url = handleImage(form.profile_image.data, profile.id, 'profile')
        profile.save()
    msg = Message(
        subject='Welcome to Our Platform!',
        recipients=[profile.email],
        sender="devlinkhub250@gmail.com",
        html=render_template('welcome_email.html', profile_setup_link='#')
        )
    from webdynamic.app import mail
    mail.send(msg)


def profileAccountUpdate(form, request, profile):
    '''update user profile account'''
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
    msg = Message(
        subject='Welcome to Our Platform!',
        recipients=[profile.email],
        sender="devlinkhub250@gmail.com",
        html=render_template('update_email.html', username=profile.username)
        )
    from webdynamic.app import mail
    mail.send(msg)