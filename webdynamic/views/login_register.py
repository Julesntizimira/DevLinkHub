from flask_login import login_user, login_required, current_user, logout_user
from flask import render_template, redirect, url_for, flash, request
from models import storage
from . import app_views
from forms.user import LoginForm
from models.user import User
from flask_bcrypt import Bcrypt


bcrypt = Bcrypt()



@app_views.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    '''login user'''
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = None
        for obj in storage.all(User).values():
            if obj.username == form.username.data:
                user = obj
                break
        if user:
            if user.password == form.password.data:
                login_user(user, remember=form.remember.data)
                if current_user.is_authenticated:
                    flash('Login successful', 'success')
                    return redirect(url_for('app_views.account'))
            else:
                # Handle the case where the user is not logged in
                flash('username or password incorrect', 'error')
                return redirect(url_for('app_views.login'))
    return render_template('login.html', form=form)


@app_views.route('/logout', methods=['GET'], strict_slashes=False)
@login_required
def logout():
    '''logout user'''
    print(current_user.username)
    logout_user()
    return redirect(url_for('app_views.login'))