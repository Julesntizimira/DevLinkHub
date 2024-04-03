'''projects views'''
from flask import request, render_template, flash, redirect, url_for
from models.project import Project, Tag
from models import storage
from . import app_views
from forms.project import ProjectForm, LinkForm
from utils.handleImage import allowed_file
from flask_login import current_user, login_required
from utils.paginate import paginate
from utils.handleProject import create_new_project, updateProjectHandler
from utils.handleProjectSearch import project_search


project_attr = [
    'title',
    'description',
    'demo_link',
    'source_link'
    ]


@app_views.route('/projects', methods=['GET'], strict_slashes=False)
def projects():
    '''all projects'''
    searchQuery = None
    if request.args.get('text'):
        searchQuery = request.args.get('text')
        projects = project_search(searchQuery)
    else:
        projects = list(storage.all(Project).values())
    page = int(request.args.get('page', 1))
    result = paginate(projects, page)
    context = {
        'items_on_page': result.get('items_on_page'),
        'total_pages': result.get('total_pages'),
        'queryPage': page,
        'custom_range': result.get('custom_range'),
        'searchQuery': searchQuery if searchQuery else None
        }
    return render_template('projects.html', **context)

@app_views.route('/single_project/<id>', methods=['GET', 'POST'], strict_slashes=False)
def single_project(id):
    project = storage.get(Project, id)
    if project:
        return render_template('single_project.html', project=project)
    else:
        return redirect(url_for('app_views.projects'))

@app_views.route('/create_project', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def create_project():
    '''create_project'''
    projects = storage.all(Project).values()
    form = ProjectForm()
    link = LinkForm() 
    form.populate_tags()
    if request.method == 'POST' and form.validate_on_submit:
        for project in projects:
            if project.title == form.title.data:
                flash('Project with the same title already exists', 'error')
                return render_template('create_update_form.html', form=form)
        if form.image.data:
            img = form.image.data
            if not allowed_file(img.filename):
                flash('image formats accepted: png, jpg, jpeg, gif', 'error')
                return render_template('create_update_form.html', form=form)
        create_new_project(request, current_user, form)
        flash('new project successfully created', 'success')
        return redirect(url_for('app_views.account'))
    return render_template('create_update_form.html', form=form, linkform=link)

@app_views.route('/update_project/<project_id>', methods=['GET', 'POST'])
@login_required
def update_project(project_id):
    '''update_project'''
    project = storage.get(Project, project_id)
    if not project:
        flash('Project not found', 'error')
        return redirect(url_for('app_views.projects'))
    form = ProjectForm(obj=project)
    form.populate_tags(current_tags=project.tags)
    if request.method == 'POST' and form.validate_on_submit():
        for pr in storage.all(Project).values():
            if pr.title == form.title.data:
                if pr.id != project.id:
                    flash('Project with the same title already exists', 'error')
                    return render_template('create_update_form.html', form=form)
                break
        if form.image.data:
            img = form.image.data
            if not allowed_file(img.filename):
                flash('image formats accepted: png, jpg, jpeg, gif', 'error')
                return render_template('create_update_form.html', form=form)
        updateProjectHandler(request, project, form)
        flash('Project updated successfully', 'success')
        return redirect(url_for('app_views.projects'))
    return render_template('create_update_form.html', form=form, project_id=project_id)


@app_views.route('/delete_project/<project_id>', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def delete_project(project_id):
    '''delete project'''
    project = storage.get(Project, project_id)
    if request.method == 'POST':
        project.delete()
        flash('project successfully deleted', 'success')
        return redirect(url_for('app_views.account'))
    return render_template('delete.html')

