from flask import Flask, jsonify, make_response
from models import storage
import os
from .views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)

@app.errorhandler(404)
def not_found_error(error):
    """ 404 Error
    ---
    responses:
      404:
        description: a resource was not found
    """
    return make_response(jsonify({'error': "Not found"}), 404)

if __name__ == '__main__':
    host = os.getenv('HOST') if os.getenv('HOST') else '0.0.0.0'
    port = os.getenv('PORT') if os.getenv('PORT') else '5100'
    app.run(port=port, host=host, debug=True)