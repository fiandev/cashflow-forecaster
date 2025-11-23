from flask import Blueprint, request, jsonify
from controllers.user_controller import UserController
from middleware import validate_json
from models import User
from middleware.auth import AuthenticationMiddleware

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["POST"])
@validate_json(["email", "password"])
def login():
    """Login user and return JWT token"""
    data = request.get_json()

    user = User.query.filter_by(email=data["email"]).first()

    if not user or user.password_hash != data["password"]:
        return jsonify({"error": "Invalid credentials"}), 401

    from app import app

    token = AuthenticationMiddleware.generate_token(user.id, app.config["SECRET_KEY"])

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
@validate_json(["email", "password_hash", "name"])
def register():
    """Register new user"""
    return UserController().store()


@auth_bp.route("/me", methods=["GET"])
def get_current_user():
    """Get current user info (requires auth token)"""
    from middleware.auth import authenticate_request

    @authenticate_request
    def _get_current_user():
        return UserController().profile()

    return _get_current_user()
