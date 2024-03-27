from flask import request, render_template, redirect, url_for, flash, session
from models.user import User
from models import storage
from . import app_views
from forms.password_reset_forms import ForgotPasswordForm, EnterResetTokenForm, NewPasswordForm
from flask_mail import Message
import random
from flask_bcrypt import Bcrypt
from datetime import datetime, timezone, timedelta

bcrypt = Bcrypt()


@app_views.route('/forgot_password',
                 methods=['GET', 'POST'], strict_slashes=False)
def forgot_password():
    '''forgot password'''
    form = ForgotPasswordForm()
    if request.method == 'POST' and form.validate_on_submit:
        email = form.email.data
        user_to_reset = None
        for user in storage.all(User).values():
            if user.email == email:
                user_to_reset = user
                break
        if user_to_reset is not None:
            token = str(random.randint(100000, 999999))
            user_id = user_to_reset.id
            session[user_id] = {
                'value': token,
                'expiry': datetime.now(timezone.utc) + timedelta(minutes=5)
                }
            msg = Message(
                subject='Password Reset Instructions!',
                recipients=[email],
                sender="devlinkhub250@gmail.com",
                html=render_template('reset_token_mail.html', token=token)
                )
            from ..app import mail
            mail.send(msg)
            flash('Password reset token sent to your email', 'success')
            return redirect(url_for('app_views.reset_token', user_id=user_id))
        else:
            flash('Email does not exist', 'error')
            form = ForgotPasswordForm(email=email)
    return render_template('forgot_password.html', form=form)


@app_views.route('/reset_token/<user_id>',
                 methods=['GET', 'POST'], strict_slashes=False)
def reset_token(user_id):
    '''user enter reset token'''
    form = EnterResetTokenForm()
    if request.method == 'POST' and form.validate_on_submit:
        token_data = session.get(user_id)
        current_time = datetime.now(timezone.utc)
        if token_data['expiry'] < current_time:
            flash('Token expired', 'error')
            return redirect(url_for('app_views.login'))
        if form.token.data == token_data.get('value'):
            return redirect(url_for('app_views.new_password', user_id=user_id))
        else:
            flash('wrong reset token', 'error')
    return render_template('reset_token_form.html', form=form)

@app_views.route('/new_password/<user_id>',
                 methods=['GET', 'POST'], strict_slashes=False)
def new_password(user_id):
    '''user enter new password'''
    form = NewPasswordForm()
    if request.method == 'POST' and form.validate_on_submit:
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        user = storage.get(User, user_id)
        setattr(user, 'password', hashed_password)
        user.save()
        flash('password reset successfully', 'success')
        return redirect(url_for('app_views.login'))
    return render_template('new_password_form.html', form=form)