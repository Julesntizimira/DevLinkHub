from flask import Blueprint


app_views = Blueprint('app_views', __name__, url_prefix='/')

from .users import *
from .projects import *
from .skills import *
from .comments import *
from .login_register import *
from .messages import *