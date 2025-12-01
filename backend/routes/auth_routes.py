from flask import Blueprint, request, jsonify
from controllers.user_controller import UserController
from controllers.business_controller import BusinessController
from middleware import validate_json
from models import User
from middleware.auth import AuthenticationMiddleware
from utils.crypto import hash_password
import os

auth_bp = Blueprint("auth", __name__)

business_controller = BusinessController()


@auth_bp.route("/login", methods=["POST"])
@validate_json(["email", "password"])
def login():
    """Login user and return JWT token"""
    data = request.get_json()

    user = User.query.filter_by(email=data["email"]).first()
    hashed_password = hash_password(data["password"])

    if not user or user.password != hashed_password:
        return jsonify({"error": "Invalid credentials"}), 401

    token = AuthenticationMiddleware.generate_token(user.id, os.getenv("SECRET_KEY"))

    return jsonify(
        {
            "token": token,
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "role": user.role,
            },
        }
    )


@auth_bp.route("/register", methods=["POST"])
@validate_json(["email", "password", "name"])
def register():
    """Register new user"""
    return UserController().bussinessOwnerStore()


@auth_bp.route("/me", methods=["GET"])
def get_current_user():
    """Get current user info (requires auth token)"""
    from middleware.auth import authenticate_request

    @authenticate_request
    def _get_current_user():
        return UserController().profile()

    return _get_current_user()


@auth_bp.route("/business/register", methods=["POST"])
def register_business():
    """Register new business for the authenticated user"""
    return business_controller.create_business()
