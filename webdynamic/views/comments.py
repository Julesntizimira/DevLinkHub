'''comment view'''
from flask import request, redirect, url_for
from models.user import Profile
from models.comment import Comment
from models import storage
from . import app_views
from flask_login import login_required, current_user


@login_required
@app_views.route('/add_comment/<project_id>',
                 methods=['GET', 'POST'], strict_slashes=False)
def add_comment(project_id):
    '''comment view'''
    profile = current_user.profile
    if request.method == 'POST':
        data = {'text': request.form.get('message'),
                'profile_id': profile.id,
                'project_id': project_id
                }
        comment = Comment(**data)
        comment.save()
        return redirect(url_for('app_views.single_project', id=project_id))
