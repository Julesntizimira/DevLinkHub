from flask import request, render_template, redirect, url_for, flash
from models.user import User
from models import storage
from . import app_views
from forms.message import MessageForm
from models.message import Message
from flask_login import login_required, current_user


@app_views.route('/inbox', methods=['GET'], strict_slashes=False)
def inbox():
    '''inbox'''
    messages = sorted(current_user.received_messages, key=lambda x: x.created_at, reverse=True)
    unread = sum(1 for message in messages if not message.is_read)
    return render_template('inbox.html', messages=messages, unread=unread)


@app_views.route('/read_message/<message_id>', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def read_message(message_id):
    message = storage.get(Message, message_id)
    message.is_read = True
    message.save()
    return render_template('message.html', message=message)



@app_views.route('/message/<receiver_id>', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def message(receiver_id):
    '''compose message'''
    receiver = storage.get(User, receiver_id)
    form = MessageForm()
    if request.method == 'POST' and form.validate_on_submit:
        data = {
            'message': request.form.get('message'),
            'subject': request.form.get('subject'),
            'receiver_id': receiver_id,
            'sender_id': current_user.id
            }
        new_message = Message(**data)
        new_message.save()
        flash('your message is successfully sent', 'success')
        return redirect(url_for('app_views.profile', profile_id=receiver.profile.id))
    return render_template('message_form.html', form=form)