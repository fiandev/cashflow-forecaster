from flask import request, jsonify
from models import db, APIKey, Business


class APIKeyController:
    @staticmethod
    def create_api_key():
        data = request.get_json()

        if not data or not data.get("business_id"):
            return jsonify({"error": "business_id is required"}), 400

        business = Business.query.get(data["business_id"])
        if not business:
            return jsonify({"error": "Business not found"}), 404

        api_key = APIKey(
            business_id=data["business_id"],
            name=data.get("name"),
            key_hash=data.get("key_hash"),
            scopes=data.get("scopes"),
            revoked=data.get("revoked", False),
        )

        db.session.add(api_key)
        db.session.commit()

        return jsonify(
            {
                "id": api_key.id,
                "business_id": api_key.business_id,
                "name": api_key.name,
                "key_hash": api_key.key_hash,
                "scopes": api_key.scopes,
                "revoked": api_key.revoked,
                "created_at": api_key.created_at.isoformat()
                if api_key.created_at
                else None,
            }
        ), 201

    @staticmethod
    def get_api_keys():
        api_keys = APIKey.query.all()
        return jsonify(
            [
                {
                    "id": key.id,
                    "business_id": key.business_id,
                    "name": key.name,
                    "key_hash": key.key_hash,
                    "scopes": key.scopes,
                    "revoked": key.revoked,
                    "created_at": key.created_at.isoformat()
                    if key.created_at
                    else None,
                }
                for key in api_keys
            ]
        )

    @staticmethod
    def get_api_key(api_key_id):
        api_key = APIKey.query.get(api_key_id)
        if not api_key:
            return jsonify({"error": "API key not found"}), 404

        return jsonify(
            {
                "id": api_key.id,
                "business_id": api_key.business_id,
                "name": api_key.name,
                "key_hash": api_key.key_hash,
                "scopes": api_key.scopes,
                "revoked": api_key.revoked,
                "created_at": api_key.created_at.isoformat()
                if api_key.created_at
                else None,
            }
        )

    @staticmethod
    def update_api_key(api_key_id):
        api_key = APIKey.query.get(api_key_id)
        if not api_key:
            return jsonify({"error": "API key not found"}), 404

        data = request.get_json()

        if "business_id" in data:
            business = Business.query.get(data["business_id"])
            if not business:
                return jsonify({"error": "Business not found"}), 404
            api_key.business_id = data["business_id"]

        if "name" in data:
            api_key.name = data["name"]

        if "key_hash" in data:
            api_key.key_hash = data["key_hash"]

        if "scopes" in data:
            api_key.scopes = data["scopes"]

        if "revoked" in data:
            api_key.revoked = data["revoked"]

        db.session.commit()

        return jsonify(
            {
                "id": api_key.id,
                "business_id": api_key.business_id,
                "name": api_key.name,
                "key_hash": api_key.key_hash,
                "scopes": api_key.scopes,
                "revoked": api_key.revoked,
                "created_at": api_key.created_at.isoformat()
                if api_key.created_at
                else None,
            }
        )

    @staticmethod
    def delete_api_key(api_key_id):
        api_key = APIKey.query.get(api_key_id)
        if not api_key:
            return jsonify({"error": "API key not found"}), 404

        db.session.delete(api_key)
        db.session.commit()

        return jsonify({"message": "API key deleted successfully"})

    @staticmethod
    def get_api_keys_by_business(business_id):
        business = Business.query.get(business_id)
        if not business:
            return jsonify({"error": "Business not found"}), 404

        api_keys = APIKey.query.filter_by(business_id=business_id).all()
        return jsonify(
            [
                {
                    "id": key.id,
                    "business_id": key.business_id,
                    "name": key.name,
                    "key_hash": key.key_hash,
                    "scopes": key.scopes,
                    "revoked": key.revoked,
                    "created_at": key.created_at.isoformat()
                    if key.created_at
                    else None,
                }
                for key in api_keys
            ]
        )

    @staticmethod
    def get_active_api_keys():
        api_keys = APIKey.query.filter_by(revoked=False).all()
        return jsonify(
            [
                {
                    "id": key.id,
                    "business_id": key.business_id,
                    "name": key.name,
                    "key_hash": key.key_hash,
                    "scopes": key.scopes,
                    "revoked": key.revoked,
                    "created_at": key.created_at.isoformat()
                    if key.created_at
                    else None,
                }
                for key in api_keys
            ]
        )

    @staticmethod
    def get_revoked_api_keys():
        api_keys = APIKey.query.filter_by(revoked=True).all()
        return jsonify(
            [
                {
                    "id": key.id,
                    "business_id": key.business_id,
                    "name": key.name,
                    "key_hash": key.key_hash,
                    "scopes": key.scopes,
                    "revoked": key.revoked,
                    "created_at": key.created_at.isoformat()
                    if key.created_at
                    else None,
                }
                for key in api_keys
            ]
        )

    @staticmethod
    def revoke_api_key(api_key_id):
        api_key = APIKey.query.get(api_key_id)
        if not api_key:
            return jsonify({"error": "API key not found"}), 404

        api_key.revoked = True
        db.session.commit()

        return jsonify(
            {
                "id": api_key.id,
                "business_id": api_key.business_id,
                "name": api_key.name,
                "key_hash": api_key.key_hash,
                "scopes": api_key.scopes,
                "revoked": api_key.revoked,
                "created_at": api_key.created_at.isoformat()
                if api_key.created_at
                else None,
            }
        )

    @staticmethod
    def activate_api_key(api_key_id):
        api_key = APIKey.query.get(api_key_id)
        if not api_key:
            return jsonify({"error": "API key not found"}), 404

        api_key.revoked = False
        db.session.commit()

        return jsonify(
            {
                "id": api_key.id,
                "business_id": api_key.business_id,
                "name": api_key.name,
                "key_hash": api_key.key_hash,
                "scopes": api_key.scopes,
                "revoked": api_key.revoked,
                "created_at": api_key.created_at.isoformat()
                if api_key.created_at
                else None,
            }
        )
