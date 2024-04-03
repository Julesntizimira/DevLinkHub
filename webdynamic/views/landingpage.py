'''the landing page view'''
from flask import render_template
from . import app_views


@app_views.route('/', methods=['GET'], strict_slashes=False)
def landingpage():
    '''display the landing page'''
    return render_template('landingpage.html')
