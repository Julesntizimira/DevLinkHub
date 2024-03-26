from flask import make_response, jsonify, request, abort, render_template, flash, redirect, url_for
from models.user import User, Profile
from models.project import Project, Tag
from models.link import Link
from models.objective import Objective
from models.takeaway import Takeaway
from models.subtitle import Subtitle
from models import storage
from . import app_views
from forms.project import ProjectForm
from utils.handleImage import handleImage
from flask_login import current_user, login_required
from utils.paginate import paginate
from utils.handleProject import update_links, update_subtitles, update_takeaways, create_links, create_subtitle, create_takeaways

project_attr = [
    'title',
    'description',
    'demo_link',
    'source_link'
    ]


@app_views.route('/projects', methods=['GET'], strict_slashes=False)
def projects():
    '''all projects'''
    projects = []
    searchQuery = None
    if request.args.get('text'):
        searchQuery = request.args.get('text').lower()
        for project in storage.all(Project).values():
            if searchQuery in project.title.lower() or (project.description and searchQuery in project.description.lower()):
                    projects.append(project)
            else:
                for tag in project.tags:
                    if searchQuery in tag.name.lower():
                        projects.append(project)
                        break
    else:
        projects = list(storage.all(Project).values())
    page = int(request.args.get('page', 1))
    # Number of projects per page
    
    items_on_page, total_pages, custom_range = paginate(projects, page)
    context = {
        'items_on_page': items_on_page,
        'total_pages': total_pages,
        'queryPage': page,
        'custom_range': custom_range,
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
    form.populate_tags()
    if request.method == 'POST' and form.validate_on_submit:
        for project in projects:
            if project.title == form.title.data:
                flash('Project with the same title already exists', 'error')
                return redirect(url_for('app_views.create_project'))
        data = { k: v for k, v in request.form.items() if k in project_attr}
        data['user_id'] = current_user.id
        new_project = Project(**data)
        new_project.image_url = handleImage(form.image.data, new_project.id)
        new_project.tags = [tag for tag in storage.all(Tag).values() if tag.id in form.tags.data]
        # create project links
        create_links(form.links.data, new_project)
        # create project subtitles and objectives
        create_subtitle(form.subtitles.data, new_project)
        # create project takeaways
        create_takeaways(form.takeaways.data, new_project)
        new_project.save()
        return redirect(url_for('app_views.account'))
    return render_template('create_update_form.html', form=form)

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
        try:
            data = { k: v for k, v in request.form.items() if k in project_attr}
            for k, v in data.items():
                setattr(project, k, v)
            if form.image.data:
                project.image_url = handleImage(form.image.data, project.id)
            # Update project tags
            project.tags = [tag for tag in storage.all(Tag).values() if tag.id in form.tags.data]
            # Save changes to the project
            project.save()
            # Update project links
            update_links(form.links.data, project)
            # Update project objectives
            update_subtitles(form.subtitles.data, project)
            # Update project takeaways
            update_takeaways(form.takeaways.data, project)
            flash('Project updated successfully', 'success')
            return redirect(url_for('app_views.projects'))
        except Exception as e:
            flash(f'Error updating project: {e}', 'error')
            # Log the error for debugging purposes
            print(f'Error updating project: {e}')
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

