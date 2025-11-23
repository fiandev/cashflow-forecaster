from flask import Blueprint, request, jsonify, g
from controllers.user_controller import UserController
from middleware import (
    authenticate_request,
    require_permission,
    validate_json,
    self_or_admin_required,
    require_role,
)

user_bp = Blueprint("users", __name__)


@user_bp.route("/", methods=["POST"])
@validate_json(["email", "password_hash"])
def create_user():
    return UserController().store()


@user_bp.route("/", methods=["GET"])
@authenticate_request
@require_permission("users:read")
def get_users():
    return UserController().index()


@user_bp.route("/<int:user_id>", methods=["GET"])
@authenticate_request
@self_or_admin_required
def get_user(user_id):
    return UserController().show(user_id)


@user_bp.route("/<int:user_id>", methods=["PUT"])
@authenticate_request
@self_or_admin_required
@validate_json()
def update_user(user_id):
    return UserController().update(user_id)


@user_bp.route("/<int:user_id>", methods=["DELETE"])
@authenticate_request
@require_role("admin")
def delete_user(user_id):
    return UserController().destroy(user_id)


# Additional User Routes
@user_bp.route("/search", methods=["GET"])
@authenticate_request
@require_permission("users:read")
def search_users():
    """Search users"""
    return UserController().search_users()


@user_bp.route("/role/<string:role>", methods=["GET"])
@authenticate_request
@require_permission("users:read")
def get_users_by_role(role):
    """Get users by role"""
    return UserController().get_users_by_role(role)
