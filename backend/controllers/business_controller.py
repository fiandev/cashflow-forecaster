from flask import request, jsonify, g
from models import db, Business, User
from repositories.business_repository import BusinessRepository
from middleware import authenticate_request


class BusinessController:
    def __init__(self):
        self.business_repository = BusinessRepository()

    def index(self):
        """Get all businesses"""
        businesses = self.business_repository.all()
        return jsonify(
            [self.business_repository.to_dict(business) for business in businesses]
        )

    def show(self, business_id):
        """Get specific business"""
        business = self.business_repository.find(business_id)
        if not business:
            return jsonify({"error": "Business not found"}), 404

        return jsonify(self.business_repository.to_dict(business))

    def store(self):
        """Create new business"""
        data = request.get_json()

        if (
            not data
            or not data.get("name")
            or not data.get("currency")
            or not data.get("owner_id")
        ):
            return jsonify({"error": "Name, currency, and owner_id are required"}), 400

        # Verify owner exists
        owner = User.query.get(data["owner_id"])
        if not owner:
            return jsonify({"error": "Owner not found"}), 404

        business = self.business_repository.createWithOwner(data, data["owner_id"])
        return jsonify(self.business_repository.to_dict(business)), 201

    def update(self, business_id):
        """Update business"""
        business = self.business_repository.find(business_id)
        if not business:
            return jsonify({"error": "Business not found"}), 404

        data = request.get_json()

        if "owner_id" in data:
            owner = User.query.get(data["owner_id"])
            if not owner:
                return jsonify({"error": "Owner not found"}), 404

        updated_business = self.business_repository.update(business_id, data)
        return jsonify(self.business_repository.to_dict(updated_business))

    def destroy(self, business_id):
        """Delete business"""
        if not self.business_repository.find(business_id):
            return jsonify({"error": "Business not found"}), 404

        self.business_repository.delete(business_id)
        return jsonify({"message": "Business deleted successfully"})

    def my_businesses(self):
        """Get current user's businesses"""
        if not hasattr(g, "current_user") or not g.current_user:
            return jsonify({"error": "Authentication required"}), 401

        businesses = self.business_repository.findByOwner(g.current_user.id)
        return jsonify(
            [self.business_repository.to_dict(business) for business in businesses]
        )

    def search(self):
        """Search businesses"""
        query = request.args.get("q", "")
        if not query:
            return jsonify({"error": "Search query is required"}), 400

        businesses = self.business_repository.search(query)
        return jsonify(
            [self.business_repository.to_dict(business) for business in businesses]
        )

    def by_country(self, country):
        """Get businesses by country"""
        businesses = self.business_repository.findByCountry(country)
        return jsonify(
            [self.business_repository.to_dict(business) for business in businesses]
        )

    def by_city(self, city):
        """Get businesses by city"""
        businesses = self.business_repository.findByCity(city)
        return jsonify(
            [self.business_repository.to_dict(business) for business in businesses]
        )

    def by_currency(self, currency):
        """Get businesses by currency"""
        businesses = self.business_repository.findByCurrency(currency)
        return jsonify(
            [self.business_repository.to_dict(business) for business in businesses]
        )

    def with_details(self, business_id):
        """Get business with all details"""
        business = self.business_repository.getWithAllRelations(business_id)
        if not business:
            return jsonify({"error": "Business not found"}), 404

        business_data = self.business_repository.to_dict(business)

        # Add related data
        business_data["owner"] = (
            {
                "id": business.owner.id,
                "name": business.owner.name,
                "email": business.owner.email,
            }
            if business.owner
            else None
        )

        business_data["categories_count"] = len(business.categories)
        business_data["transactions_count"] = len(business.transactions)
        business_data["forecasts_count"] = len(business.forecasts)
        business_data["alerts_count"] = len(business.alerts)

        return jsonify(business_data)

    def update_settings(self, business_id):
        """Update business settings"""
        business = self.business_repository.find(business_id)
        if not business:
            return jsonify({"error": "Business not found"}), 404

        data = request.get_json()
        if "settings" not in data:
            return jsonify({"error": "Settings are required"}), 400

        updated_business = self.business_repository.updateSettings(
            business_id, data["settings"]
        )
        return jsonify(self.business_repository.to_dict(updated_business))
