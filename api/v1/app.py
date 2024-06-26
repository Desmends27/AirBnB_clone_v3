#!/usr/bin/python3
""" flask application  instance created here"""
from flask import Flask, jsonify
from flask import Blueprint
from models import storage
from api.v1.views import app_views
from flask_cors import CORS
import os

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, origin="0.0.0.0")

@app.teardown_appcontext
def storage_close(exception):
    """ Calls the storage.close method """
    storage.close()

@app.errorhandler(404)
def error404(e):
    """ Prints a not found for incorrect url's """
    error = {
            "error" : "Not found"
            }
    return jsonify(error), 404


if __name__ == "__main__":
    host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
    port = int(os.environ.get('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
