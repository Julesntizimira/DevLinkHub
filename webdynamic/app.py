from markupsafe import Markup
from flask import Flask, render_template
import os
from .views import app_views
from flask_login import LoginManager, current_user
from models import storage
from models.user import User
from flask_mail import Mail
from flask_cors import CORS
from dotenv import load_dotenv


app = Flask(__name__)
CORS(app)

load_dotenv()

secret_key = os.urandom(24)
app.config['SECRET_KEY'] = str(secret_key)


def linebreaksbr(value):
    """Convert newlines to <br> tags."""
    return Markup(value.replace('\n', '<br>'))
app.jinja_env.filters['linebreaksbr'] =  linebreaksbr


# Configure Flask-Mail settings
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER') # SMTP server address
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))  # SMTP port (usually 587 for TLS/STARTTLS)
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS').lower() in ['true', '1', 'yes'] # Enable TLS encryption
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME') # SMTP username
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD') # SMTP password
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER') # Default sender email address


# Initialize Flask-Mail
mail = Mail(app)

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


@app.errorhandler(404)
def not_found_error(error):
    '''not found page'''
    return render_template('notfound.html')


if __name__ == '__main__':
    host = os.getenv('HOST') if os.getenv('HOST') else '0.0.0.0'
    port = os.getenv('PORT') if os.getenv('PORT') else '5200'
    app.run(port=port, host=host, debug=True)