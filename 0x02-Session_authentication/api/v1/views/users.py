#!/usr/bin/env python3
"""
Module that contains the views to manage users
"""
from api.v1.views import app_views
from models.user import User
from flask import abort, jsonify, request


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def get_all_users() -> str:
    """
    Get all users
    """
    users = [user.to_json() for user in User.all()]
    return jsonify(users)


@app_views.route("/users/<user_id>", methods=["GET"], strict_slashes=False)
def get_one_user(user_id: str = None) -> str:
    """
    Get user
    """
    if user_id is None:
        abort(404)
    if user_id == "me":
        if not request.current_user:
            abort(404)
        else:
            return jsonify(request.current_user.to_json())
    user = User.get(user_id)
    if not user:
        abort(404)
    return jsonify(user.to_json())


@app_views.route("/users/<user_id>", methods=["DELETE"], strict_slashes=False)
def delete_user(user_id: str = None) -> str:
    """
    Delete a user
    """
    if not user_id :
        abort(404)
    user = User.get(user_id)
    if not user :
        abort(404)
    user.remove()
    return jsonify({}), 200


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_user() -> str:
    """
    Create a user
    """
    json_req = None
    error_msg = None
    try:
        json_req = request.get_json()
    except Exception as error:
        json_req = None
    if json_req is None or json_req.get("email", "") == "":
        error_msg = "email missing"
    if error_msg is None and json_req.get("password", "") == "":
        error_msg = "password missing"
    if error_msg is None:
        try:
            user = User()
            user.email = json_req.get("email")
            user.password = json_req.get("password")
            user.first_name = json_req.get("first_name")
            user.last_name = json_req.get("last_name")
            user.save()
            return jsonify(user.to_json()), 201
        except Exception as error:
            error_msg = f"Can't create User: {error}"
    return jsonify({"error": error_msg}), 400


@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def update_user(user_id: str = None) -> str:
    """
    Update a user
    """
    if user_id is None:
        abort(404)
    user = User.get(user_id)
    if user is None:
        abort(404)
    json_req = None
    try:
        json_req = request.get_json()
    except Exception:
        json_req = None
    if json_req is None:
        return jsonify({"error": "Wrong format"}), 400
    if json_req.get("first_name") is not None:
        user.first_name = json_req.get("first_name")
    if json_req.get("last_name") is not None:
        user.last_name = json_req.get("last_name")
    user.save()
    return jsonify(user.to_json()), 200
