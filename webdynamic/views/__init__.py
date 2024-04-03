from flask import Blueprint

# create blueprint
app_views = Blueprint('app_views', __name__, url_prefix='/')

from .users import *
from .projects import *
from .skills import *
from .comments import *
from .login_register import *
from .messages import *
from .password_reset import *
from .landingpage import *