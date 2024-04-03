'''comment view'''
from flask import request, redirect, url_for, flash
from models.user import Profile
from models.comment import Comment
from models import storage
from . import app_views
from flask_login import login_required, current_user



@app_views.route('/add_comment/<project_id>',
                 methods=['GET', 'POST'], strict_slashes=False)
@login_required
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



@app_views.route('/delete_comment/<comment_id>/<project_id>',
                 methods=['GET', 'POST'], strict_slashes=False)
@login_required
def delete_comment(comment_id, project_id):
    '''delete comment'''
    comment = storage.get(Comment, comment_id)
    comment.delete()
    flash('Comment deleted successfully', 'success')
    return redirect(url_for('app_views.single_project', id=project_id))
