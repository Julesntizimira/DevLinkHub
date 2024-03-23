from flask import request, abort, render_template, redirect, url_for, flash
from models.user import Profile
from models.project import Project
from models.comment import Comment
from models import storage
from . import app_views


@app_views.route('/add_comment/<project_id>', methods=['GET', 'POST'], strict_slashes=False)
def add_comment(project_id):
    '''add skill'''
    profile = storage.get(Profile, 'f9aa840f-26f4-4ded-8fb3-d1829dd1f356')
    if request.method == 'POST':
        data = {'text': request.form.get('message'),
                'profile_id': profile.id,
                'project_id': project_id
                }
        comment = Comment(**data)
        comment.save()
        return redirect(url_for('app_views.single_project', id=project_id))
    