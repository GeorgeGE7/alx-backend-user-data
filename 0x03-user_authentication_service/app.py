#!/usr/bin/env python3
"""Route module for basic flask app API
"""

from flask import Flask, abort, jsonify, redirect, request
from flask.helpers import make_response

from auth import Auth
from db import DB
from user import User

AUTH = Auth()

app = Flask(__name__)


@app.route("/users", methods=["POST"], strict_slashes=False)
def users() -> str:
    """Register a user and return a JSON response"""
    body_password = request.form.get("password")
    body_email = request.form.get("email")
    try:
        AUTH.register_user(body_email, body_password)
        return jsonify({"email": body_email, "message": "User created"})
    except Exception:
        return jsonify({"message": "Email already registered"}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login():
    """Validate user credentials and return a JSON response"""
    req = request.form
    body_password = req.get("password", "")
    body_email = req.get("email", "")
    check_log = AUTH.valid_login(body_email, body_password)
    if not check_log:
        abort(401)
    res = make_response(jsonify({"email": body_email, "message": "Logged in"}))
    res.set_cookie("session_id", AUTH.create_session(body_email))
    return res


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout():
    """Delete the session ID"""
    session_id = request.cookies.get("session_id", None)
    user_from_session = AUTH.get_user_from_session_id(session_id)
    if session_id is None or user_from_session is None:
        abort(403)
    AUTH.destroy_session(user_from_session.id)
    return redirect("/")


@app.route("/profile", methods=["GET"], strict_slashes=False)
def get_profile() -> str:
    """Return user information if session ID is valid"""
    u_cookie = request.cookies.get("session_id", None)
    user = AUTH.get_user_from_session_id(u_cookie)
    if u_cookie is None or user is None:
        abort(403)
    return jsonify({"email": user}), 200


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token_route() -> str:
    """Return a reset password token if the email is registered"""
    user_req = request.form
    body_emai = user_req.get("email", "")
    is_exists = AUTH.create_session(body_emai)
    if not is_exists:
        abort(403)
    token = AUTH.get_reset_password_token(body_emai)
    return jsonify({"email": body_emai, "reset_token": token})


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password() -> str:
    """Update the user password if the token is valid"""
    body_emai = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")
    try:
        AUTH.update_password(reset_token, new_password)
    except Exception:
        abort(403)
    return jsonify({"email": body_emai, "message": "Password updated"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
