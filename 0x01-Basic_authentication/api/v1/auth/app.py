#!/usr/bin/env python3
"""
API Route Module
This module sets up the Flask API, defining routing, error handling,
and pre-request authentication based on specified environment settings.
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
    Pre-request Handler
    Filters requests prior to route handling to verify authorization.
    Excludes specific routes from authentication based on the route list.
    Returns:
        Aborts request with 401 if authorization header is missing.
        Aborts request with 403 if user is unauthorized.
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
    404 Error Handler
    Returns a JSON response with an error message for routes not found.
    Args:
        error: The error triggered by the request.
    Returns:
        JSON response with error message and 404 status.
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """
    401 Unauthorized Error Handler
    Returns a JSON response indicating unauthorized access.
    Args:
        error: The error triggered by the request.
    Returns:
        JSON response with error message and 401 status.
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """
    403 Forbidden Error Handler
    Returns a JSON response indicating forbidden access.
    Args:
        error: The error triggered by the request.
    Returns:
        JSON response with error message and 403 status.
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
