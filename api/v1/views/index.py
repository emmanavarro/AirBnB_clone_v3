#!/usr/bin/python3
"""
Index file of views packages
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def status():
    """
    Return json with Ok status for /status route
    """
    return jsonify({'status': 'OK'})
