#!/usr/bin/env python3
"""
API Route Module
Configures the Flask API, establishes routing, error handling, and
pre-request authentication based on environment settings.
"""

from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import CORS
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth = None
AUTH_TYPE = os.getenv("AUTH_TYPE")
if AUTH_TYPE == "auth":
    from api.v1.auth.auth import Auth
    auth = Auth()
elif AUTH_TYPE == "basic_auth":
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()


@app.before_request
def bef_req():
    """
    Pre-Request Authentication Filter
    Executes before each request to verify authorization.
    Routes listed in `excluded_paths` bypass this filter.
    Actions:
        - Aborts the request with a 401 error if the authorization header is missing.
        - Aborts the request with a 403 error if the user is not authorized.
    """
    if auth is not None:
        excluded_paths = [
            '/api/v1/status/',
            '/api/v1/unauthorized/',
            '/api/v1/forbidden/'
        ]
        if auth.require_auth(request.path, excluded_paths):
            if auth.authorization_header(request) is None:
                abort(401, description="Unauthorized")
            if auth.current_user(request) is None:
                abort(403, description="Forbidden")


@app.errorhandler(404)
def not_found(error) -> str:
    """
    404 Not Found Error Handler
    Provides a JSON response for routes that do not exist.
    Args:
        error: The error encountered.
    Returns:
        JSON response containing error message and 404 status code.
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """
    401 Unauthorized Error Handler
    Returns a JSON response when the user is not authorized.
    Args:
        error: The error encountered.
    Returns:
        JSON response with an error message and a 401 status code.
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """
    403 Forbidden Error Handler
    Returns a JSON response when access is forbidden.
    Args:
        error: The error encountered.
    Returns:
        JSON response with an error message and a 403 status code.
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
