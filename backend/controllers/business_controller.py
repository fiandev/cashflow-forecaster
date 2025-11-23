from flask import request, jsonify
from models import db, Business, User


class BusinessController:
    @staticmethod
    def create_business():
        data = request.get_json()

        if (
            not data
            or not data.get("name")
            or not data.get("currency")
            or not data.get("owner_id")
        ):
            return jsonify({"error": "Name, currency, and owner_id are required"}), 400

        owner = User.query.get(data["owner_id"])
        if not owner:
            return jsonify({"error": "Owner not found"}), 404

        business = Business(
            owner_id=data["owner_id"],
            name=data["name"],
            country=data.get("country"),
            city=data.get("city"),
            currency=data["currency"],
            timezone=data.get("timezone", "Asia/Jakarta"),
            settings=data.get("settings"),
        )

        db.session.add(business)
        db.session.commit()

        return jsonify(
            {
                "id": business.id,
                "owner_id": business.owner_id,
                "name": business.name,
                "country": business.country,
                "city": business.city,
                "currency": business.currency,
                "timezone": business.timezone,
                "created_at": business.created_at.isoformat()
                if business.created_at
                else None,
                "settings": business.settings,
            }
        ), 201

    @staticmethod
    def get_businesses():
        businesses = Business.query.all()
        return jsonify(
            [
                {
                    "id": business.id,
                    "owner_id": business.owner_id,
                    "name": business.name,
                    "country": business.country,
                    "city": business.city,
                    "currency": business.currency,
                    "timezone": business.timezone,
                    "created_at": business.created_at.isoformat()
                    if business.created_at
                    else None,
                    "settings": business.settings,
                }
                for business in businesses
            ]
        )

    @staticmethod
    def get_business(business_id):
        business = Business.query.get(business_id)
        if not business:
            return jsonify({"error": "Business not found"}), 404

        return jsonify(
            {
                "id": business.id,
                "owner_id": business.owner_id,
                "name": business.name,
                "country": business.country,
                "city": business.city,
                "currency": business.currency,
                "timezone": business.timezone,
                "created_at": business.created_at.isoformat()
                if business.created_at
                else None,
                "settings": business.settings,
            }
        )

    @staticmethod
    def update_business(business_id):
        business = Business.query.get(business_id)
        if not business:
            return jsonify({"error": "Business not found"}), 404

        data = request.get_json()

        if "owner_id" in data:
            owner = User.query.get(data["owner_id"])
            if not owner:
                return jsonify({"error": "Owner not found"}), 404
            business.owner_id = data["owner_id"]

        if "name" in data:
            business.name = data["name"]

        if "country" in data:
            business.country = data["country"]

        if "city" in data:
            business.city = data["city"]

        if "currency" in data:
            business.currency = data["currency"]

        if "timezone" in data:
            business.timezone = data["timezone"]

        if "settings" in data:
            business.settings = data["settings"]

        db.session.commit()

        return jsonify(
            {
                "id": business.id,
                "owner_id": business.owner_id,
                "name": business.name,
                "country": business.country,
                "city": business.city,
                "currency": business.currency,
                "timezone": business.timezone,
                "created_at": business.created_at.isoformat()
                if business.created_at
                else None,
                "settings": business.settings,
            }
        )

    @staticmethod
    def delete_business(business_id):
        business = Business.query.get(business_id)
        if not business:
            return jsonify({"error": "Business not found"}), 404

        db.session.delete(business)
        db.session.commit()

        return jsonify({"message": "Business deleted successfully"})

    @staticmethod
    def get_businesses_by_owner(owner_id):
        owner = User.query.get(owner_id)
        if not owner:
            return jsonify({"error": "Owner not found"}), 404

        businesses = Business.query.filter_by(owner_id=owner_id).all()
        return jsonify(
            [
                {
                    "id": business.id,
                    "owner_id": business.owner_id,
                    "name": business.name,
                    "country": business.country,
                    "city": business.city,
                    "currency": business.currency,
                    "timezone": business.timezone,
                    "created_at": business.created_at.isoformat()
                    if business.created_at
                    else None,
                    "settings": business.settings,
                }
                for business in businesses
            ]
        )
