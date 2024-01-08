#!/usr/bin/python3
"""
flask app
"""

from api.v1.views import app_views
from flask import Flask, make_response, jsonify
from flask_cors import CORS
from models import storage
from os import getenv


# Flask app instance
app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})


@app.errorhandler(404)
def error_page(error):
    """
    handls for 404 errors, returns a JSON-formatted.
    """
    return make_response(jsonify({"error": "Not found"}), 404)


@app.teardown_appcontext
def close_(obj):
    """
    calls storage.close()
    """
    storage.close()


if __name__ == "__main__":

    host = getenv('HBNB_API_HOST', default='0.0.0.0')
    port = getenv('HBNB_API_PORT', default=5000)
    app.run(host, int(port), threaded=True)
