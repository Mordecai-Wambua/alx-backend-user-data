#!/usr/bin/env python3
"""Handles all routes for the Session Authentication."""
from api.v1.views import app_views
from flask import request, jsonify, make_response
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session() -> str:
    """Flask view for Session authentication."""
    email = request.form.get('email')
    if not email:
        return jsonify({"error": "email missing"}), 400

    password = request.form.get('password')
    if not password:
        return jsonify({"error": "password missing"}), 400

    user = User.search({'email': email})
    if not user:
        return jsonify({"error": "no user found for this email"}), 404

    obj = user[0]
    if not obj.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    session_id = auth.create_session(obj.id)
    response = make_response(obj.to_json())
    response.set_cookie(getenv('SESSION_NAME'), session_id)
    return response
