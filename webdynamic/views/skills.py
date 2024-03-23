from flask import request, abort, render_template, redirect, url_for, flash
from models.user import Profile, Skill
from models import storage
from . import app_views
from forms.user import SkillForm

@app_views.route('/add_skill', methods=['GET', 'POST'], strict_slashes=False)
def add_skill():
    '''add skill'''
    profile = storage.get(Profile, 'f9aa840f-26f4-4ded-8fb3-d1829dd1f356')
    form = SkillForm()
    if request.method == 'POST' and form.validate_on_submit:
        name = form.name.data.lower()
        for skill in profile.skills:
            if skill.name == name:
                flash('skill already exist', 'error')
                return redirect(url_for('app_views.account'))
        data = {
            'name': form.name.data.lower(),
            'description': form.description.data,
            'profile_id': profile.id
            }
        skill = Skill(**data)
        skill.save()
        return redirect(url_for('app_views.account'))
    return render_template('create_update_form.html', form=form)


@app_views.route('/update_skill/<skill_id>', methods=['GET', 'POST'], strict_slashes=False)
def update_skill(skill_id):
    '''update skill'''
    profile = storage.get(Profile, 'f9aa840f-26f4-4ded-8fb3-d1829dd1f356')
    skill = storage.get(Skill, skill_id)
    form = SkillForm(obj=skill)
    if request.method == 'POST' and form.validate_on_submit:
        name = form.name.data.lower()
        for skill_obj in profile.skills:
            if skill_obj.name == name and skill_obj.id != skill_id:
                flash('skill already exist', 'error')
                return redirect(url_for('app_views.account'))
        data = request.form
        for attr, val in data.items():
            setattr(skill, attr, val)
        skill.save()
        return redirect(url_for('app_views.account'))
    return render_template('create_update_form.html', form=form)

@app_views.route('/delete_skill/<skill_id>', methods=['GET', 'POST'], strict_slashes=False)
def delete_skill(skill_id):
    '''delete skill'''
    skill = storage.get(Skill, skill_id)
    if request.method == 'POST':
        skill.delete()
        flash('project successfully deleted', 'success')
        return redirect(url_for('app_views.account'))
    return render_template('delete.html')