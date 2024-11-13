#!/usr/bin/env python3
"""
Index Views Module
Defines routes to check API status, raise specific errors,
and retrieve object statistics.
"""

from flask import jsonify, abort
from api.v1.views import app_views


@app_views.route('/unauthorized', methods=['GET'], strict_slashes=False)
def authorized() -> str:
    """
    GET /api/v1/unauthorized
    Raises a 401 Unauthorized error.
    Return:
        - Aborts the request with a 401 status and an "Unauthorized" message.
    """
    abort(401, description="Unauthorized")


@app_views.route('/forbidden', methods=['GET'], strict_slashes=False)
def forbid() -> str:
    """
    GET /api/v1/forbidden
    Raises a 403 Forbidden error.
    Return:
        - Aborts the request with a 403 status and a "Forbidden" message.
    """
    abort(403, description="Forbidden")


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status() -> str:
    """
    GET /api/v1/status
    Checks the API status.
    Return:
        - JSON response with the API status as {"status": "OK"}.
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats/', strict_slashes=False)
def stats() -> str:
    """
    GET /api/v1/stats
    Retrieves the count of each object type in the database.
    Return:
        - JSON response with the number of each object, e.g., {"users": count}.
    """
    from models.user import User
    stats = {}
    stats['users'] = User.count()
    return jsonify(stats)
