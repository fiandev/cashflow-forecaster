from flask import request, jsonify, g
from models import db, User
from repositories.user_repository import UserRepository
from middleware import authenticate_request


class UserController:
    def __init__(self):
        self.user_repository = UserRepository()

    def index(self):
        """Get all users"""
        users = self.user_repository.all()
        return jsonify([self.user_repository.to_dict(user) for user in users])

    def show(self, user_id):
        """Get specific user"""
        user = self.user_repository.find(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        return jsonify(self.user_repository.to_dict(user))

    def store(self):
        """Create new user"""
        data = request.get_json()

        if not data or not data.get("email") or not data.get("password_hash"):
            return jsonify({"error": "Email and password_hash are required"}), 400

        if self.user_repository.exists(email=data["email"]):
            return jsonify({"error": "Email already exists"}), 400

        user = self.user_repository.create(data)
        return jsonify(self.user_repository.to_dict(user)), 201

    def update(self, user_id):
        """Update user"""
        user = self.user_repository.find(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        data = request.get_json()

        if "email" in data:
            if (
                self.user_repository.exists(email=data["email"])
                and data["email"] != user.email
            ):
                return jsonify({"error": "Email already exists"}), 400

        updated_user = self.user_repository.update(user_id, data)
        return jsonify(self.user_repository.to_dict(updated_user))

    def destroy(self, user_id):
        """Delete user"""
        if not self.user_repository.find(user_id):
            return jsonify({"error": "User not found"}), 404

        self.user_repository.delete(user_id)
        return jsonify({"message": "User deleted successfully"})

    def profile(self):
        """Get current user profile"""
        if not hasattr(g, "current_user") or not g.current_user:
            return jsonify({"error": "Authentication required"}), 401

        user = self.user_repository.getWithBusinesses(g.current_user.id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        profile_data = self.user_repository.to_dict(user)

        # Add related data
        profile_data["businesses"] = [
            {
                "id": business.id,
                "name": business.name,
                "country": business.country,
                "city": business.city,
                "currency": business.currency,
                "created_at": business.created_at.isoformat()
                if business.created_at
                else None,
            }
            for business in user.businesses
        ]

        profile_data["scenarios"] = [
            {
                "id": scenario.id,
                "name": scenario.name,
                "created_at": scenario.created_at.isoformat()
                if scenario.created_at
                else None,
            }
            for scenario in user.scenarios
        ]

        # Add permissions based on role
        from middleware.permissions import PermissionPolicies

        permissions = PermissionPolicies.get_user_permissions(user)
        profile_data["permissions"] = permissions

        # Add authentication method
        profile_data["auth_method"] = getattr(g, "auth_method", None)

        return jsonify(profile_data)

    def update_profile(self):
        """Update current user profile"""
        if not hasattr(g, "current_user") or not g.current_user:
            return jsonify({"error": "Authentication required"}), 401

        data = request.get_json()
        allowed_fields = ["name", "email"]
        update_data = {k: v for k, v in data.items() if k in allowed_fields}

        if not update_data:
            return jsonify({"error": "No valid fields to update"}), 400

        if "email" in update_data:
            if (
                self.user_repository.exists(email=update_data["email"])
                and update_data["email"] != g.current_user.email
            ):
                return jsonify({"error": "Email already exists"}), 400

        updated_user = self.user_repository.update(g.current_user.id, update_data)
        return jsonify(self.user_repository.to_dict(updated_user))

    def change_password(self):
        """Change current user password"""
        if not hasattr(g, "current_user") or not g.current_user:
            return jsonify({"error": "Authentication required"}), 401

        data = request.get_json()

        if not data or not data.get("current_password") or not data.get("new_password"):
            return jsonify(
                {"error": "Current password and new password are required"}
            ), 400

        # In a real app, you'd verify the current password hash
        # For now, we'll just update it
        updated_user = self.user_repository.update(
            g.current_user.id,
            {
                "password_hash": data["new_password"]  # In real app, hash this!
            },
        )

        return jsonify({"message": "Password updated successfully"})

    def search_users(self):
        """Search users"""
        query = request.args.get("q", "")
        if not query:
            return jsonify({"error": "Search query is required"}), 400

        users = self.user_repository.search(query)
        return jsonify([self.user_repository.to_dict(user) for user in users])

    def get_users_by_role(self, role):
        """Get users by role"""
        users = self.user_repository.findByRole(role)
        return jsonify([self.user_repository.to_dict(user) for user in users])
