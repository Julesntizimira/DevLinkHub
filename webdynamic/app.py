from markupsafe import Markup
from flask import Flask
import os
from .views import app_views
from flask_migrate import Migrate



app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'

def linebreaksbr(value):
    """Convert newlines to <br> tags."""
    return Markup(value.replace('\n', '<br>'))
app.jinja_env.filters['linebreaksbr'] =  linebreaksbr

app.register_blueprint(app_views)

from models.basemodel import Base
migrate = Migrate(app, Base)


if __name__ == '__main__':
    host = os.getenv('HOST') if os.getenv('HOST') else '0.0.0.0'
    port = os.getenv('PORT') if os.getenv('PORT') else '5200'
    app.run(port=port, host=host, debug=True)