from flask import Blueprint, request, jsonify, g
from controllers.user_controller import UserController
from middleware import (
    authenticate_request,
    require_permission,
    validate_json,
    self_or_admin_required,
    require_role,
)

profile_bp = Blueprint("profile", __name__)


@profile_bp.route("/", methods=["GET"])
@authenticate_request
def get_profile():
    """Get current user profile"""
    return UserController().profile()


@profile_bp.route("/", methods=["PUT"])
@authenticate_request
@validate_json()
def update_profile():
    """Update current user profile"""
    return UserController().update_profile()


@profile_bp.route("/change-password", methods=["POST"])
@authenticate_request
@validate_json(["current_password", "new_password"])
def change_password():
    """Change current user password"""
    return UserController().change_password()
