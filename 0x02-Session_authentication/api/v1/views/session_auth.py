#!/usr/bin/env python3
""" Module of Session Authentication views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_login():
    """handles user login
    """
    email = request.form.get('email')
    if email is None:
        return jsonify({"error": "email missing"}), 400
    password = request.form.get('password')
    if password is None:
        return jsonify({"error": "password missing"}), 400

    users = User.search({'email': email})
    if len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    user = users[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth

    session_id = auth.create_session(user.id)
    res = jsonify(user.to_json())
    res.set_cookie(os.getenv('SESSION_NAME', session_id))

    return res


@app_views.route('auth_session/logout',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_session():
    from api.v1.app import auth

    deleted = auth.destroy_session(request)
    if deleted:
        return jsonify({}), 200
    else:
        abort(404)
