from flask import request, jsonify
from models import db, User
from datetime import datetime


class UserController:
    @staticmethod
    def create_user():
        data = request.get_json()

        if not data or not data.get("email") or not data.get("password_hash"):
            return jsonify({"error": "Email and password_hash are required"}), 400

        if User.query.filter_by(email=data["email"]).first():
            return jsonify({"error": "Email already exists"}), 400

        user = User(
            email=data["email"],
            password_hash=data["password_hash"],
            name=data.get("name"),
            role=data.get("role"),
        )

        db.session.add(user)
        db.session.commit()

        return jsonify(
            {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "role": user.role,
                "created_at": user.created_at.isoformat() if user.created_at else None,
            }
        ), 201

    @staticmethod
    def get_users():
        users = User.query.all()
        return jsonify(
            [
                {
                    "id": user.id,
                    "email": user.email,
                    "name": user.name,
                    "role": user.role,
                    "created_at": user.created_at.isoformat()
                    if user.created_at
                    else None,
                    "last_login": user.last_login.isoformat()
                    if user.last_login
                    else None,
                }
                for user in users
            ]
        )

    @staticmethod
    def get_user(user_id):
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        return jsonify(
            {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "role": user.role,
                "created_at": user.created_at.isoformat() if user.created_at else None,
                "last_login": user.last_login.isoformat() if user.last_login else None,
            }
        )

    @staticmethod
    def update_user(user_id):
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        data = request.get_json()

        if "email" in data:
            existing_user = User.query.filter_by(email=data["email"]).first()
            if existing_user and existing_user.id != user_id:
                return jsonify({"error": "Email already exists"}), 400
            user.email = data["email"]

        if "password_hash" in data:
            user.password_hash = data["password_hash"]

        if "name" in data:
            user.name = data["name"]

        if "role" in data:
            user.role = data["role"]

        if "last_login" in data:
            user.last_login = (
                datetime.fromisoformat(data["last_login"])
                if data["last_login"]
                else None
            )

        db.session.commit()

        return jsonify(
            {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "role": user.role,
                "created_at": user.created_at.isoformat() if user.created_at else None,
                "last_login": user.last_login.isoformat() if user.last_login else None,
            }
        )

    @staticmethod
    def delete_user(user_id):
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        db.session.delete(user)
        db.session.commit()

        return jsonify({"message": "User deleted successfully"})
