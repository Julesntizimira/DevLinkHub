from flask import make_response, jsonify, request, abort, render_template, flash, redirect, url_for
from models.user import User, Profile
from models.project import Project, Tag
from models import storage
from . import app_views
from forms.project import ProjectForm
from utils.handleImage import handleImage

project_attr = [
    'title',
    'description',
    'demo_link',
    'source_link'
    ]


@app_views.route('/projects', methods=['GET'], strict_slashes=False)
def projects():
    '''all projects'''
    projects = storage.all(Project).values()
    return render_template('projects.html', projects=projects)

@app_views.route('/single_project/<id>', methods=['GET', 'POST'], strict_slashes=False)
def single_project(id):
    project = storage.get(Project, id)
    if project:
        return render_template('single_project.html', project=project)
    else:
        return redirect(url_for('app_views.projects'))

@app_views.route('/create_project', methods=['GET', 'POST'], strict_slashes=False)
def create_project():
    '''create_project'''
    projects = [project.to_dict() for project in storage.all(Project).values()]
    form = ProjectForm()
    form.populate_tags()
    if request.method == 'POST' and form.validate_on_submit:
        for project in projects:
            if project.get('title') == form.title.data:
                flash('Project with the same title already exists', 'error')
                return redirect(url_for('app_views.create_project'))
        data = { k: v for k, v in request.form.items() if k in project_attr}
        data['user_id'] = 'b0096a30-1dbf-42ad-b985-9f7ad7036fce'
        new_project = Project(**data)
        new_project.image_url = handleImage(form.image.data, new_project.id)
        new_project.tags = [tag for tag in storage.all(Tag).values() if tag.id in form.tags.data]
        new_project.save()
        return redirect(url_for('app_views.projects'))
    return render_template('create_update_form.html', form=form)

@app_views.route('/update_project/<project_id>', methods=['GET', 'POST'])
def update_project(project_id):
    '''update_project'''
    project = storage.get(Project, project_id)
    if not project:
        flash('Project not found', 'error')
        return redirect(url_for('app_views.projects'))

    form = ProjectForm(obj=project)
    current_tags = project.tags
    form.populate_tags(current_tags)
    if request.method == 'POST' and form.validate_on_submit():
        # form.populate_obj(project)
        if form.image.data:
            project.image_url = handleImage(form.image.data, project.id)
        data = { k: v for k, v in request.form.items() if k in project_attr}
        for attr, val in data.items():
            setattr(project, attr, val)
        project.tags = [tag for tag in storage.all(Tag).values() if tag.id in form.tags.data]
        for tag in project.tags:
            print(tag)
        project.save()
        flash('Project updated successfully', 'success')
        return redirect(url_for('app_views.projects'))
    
    return render_template('create_update_form.html', form=form, project_id=project_id)


@app_views.route('/delete_project/<project_id>', methods=['GET', 'POST'], strict_slashes=False)
def delete_project(project_id):
    '''delete project'''
    project = storage.get(Project, project_id)
    if request.method == 'POST':
        project.delete()
        flash('project successfully deleted', 'success')
        return redirect(url_for('app_views.account'))
    return render_template('delete.html')

