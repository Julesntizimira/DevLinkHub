from markupsafe import Markup
from flask import Flask
import os
from .views import app_views
from flask_login import LoginManager, current_user
from models import storage
from models.user import User


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'


def linebreaksbr(value):
    """Convert newlines to <br> tags."""
    return Markup(value.replace('\n', '<br>'))
app.jinja_env.filters['linebreaksbr'] =  linebreaksbr

app.register_blueprint(app_views)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "app_views.login"

@login_manager.user_loader
def load_user(user_id):
    '''load user'''
    user = storage.get(User, user_id)
    return user

# Context processor to add current_user to template context
@app.context_processor
def inject_user():
    return dict(current_user=current_user)

if __name__ == '__main__':
    host = os.getenv('HOST') if os.getenv('HOST') else '0.0.0.0'
    port = os.getenv('PORT') if os.getenv('PORT') else '5200'
    app.run(port=port, host=host, debug=True)