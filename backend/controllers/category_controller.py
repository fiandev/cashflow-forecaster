from flask import request, jsonify
from models import db, Category, Business


class CategoryController:
    @staticmethod
    def create_category():
        data = request.get_json()

        if (
            not data
            or not data.get("name")
            or not data.get("type")
            or not data.get("business_id")
        ):
            return jsonify({"error": "Name, type, and business_id are required"}), 400

        business = Business.query.get(data["business_id"])
        if not business:
            return jsonify({"error": "Business not found"}), 404

        if "parent_id" in data and data["parent_id"]:
            parent = Category.query.get(data["parent_id"])
            if not parent:
                return jsonify({"error": "Parent category not found"}), 404

        category = Category(
            business_id=data["business_id"],
            name=data["name"],
            type=data["type"],
            parent_id=data.get("parent_id"),
        )

        db.session.add(category)
        db.session.commit()

        return jsonify(
            {
                "id": category.id,
                "business_id": category.business_id,
                "name": category.name,
                "type": category.type,
                "parent_id": category.parent_id,
                "created_at": category.created_at.isoformat()
                if category.created_at
                else None,
            }
        ), 201

    @staticmethod
    def get_categories():
        categories = Category.query.all()
        return jsonify(
            [
                {
                    "id": category.id,
                    "business_id": category.business_id,
                    "name": category.name,
                    "type": category.type,
                    "parent_id": category.parent_id,
                    "created_at": category.created_at.isoformat()
                    if category.created_at
                    else None,
                }
                for category in categories
            ]
        )

    @staticmethod
    def get_category(category_id):
        category = Category.query.get(category_id)
        if not category:
            return jsonify({"error": "Category not found"}), 404

        return jsonify(
            {
                "id": category.id,
                "business_id": category.business_id,
                "name": category.name,
                "type": category.type,
                "parent_id": category.parent_id,
                "created_at": category.created_at.isoformat()
                if category.created_at
                else None,
            }
        )

    @staticmethod
    def update_category(category_id):
        category = Category.query.get(category_id)
        if not category:
            return jsonify({"error": "Category not found"}), 404

        data = request.get_json()

        if "business_id" in data:
            business = Business.query.get(data["business_id"])
            if not business:
                return jsonify({"error": "Business not found"}), 404
            category.business_id = data["business_id"]

        if "name" in data:
            category.name = data["name"]

        if "type" in data:
            category.type = data["type"]

        if "parent_id" in data:
            if data["parent_id"]:
                parent = Category.query.get(data["parent_id"])
                if not parent:
                    return jsonify({"error": "Parent category not found"}), 404
            category.parent_id = data["parent_id"]

        db.session.commit()

        return jsonify(
            {
                "id": category.id,
                "business_id": category.business_id,
                "name": category.name,
                "type": category.type,
                "parent_id": category.parent_id,
                "created_at": category.created_at.isoformat()
                if category.created_at
                else None,
            }
        )

    @staticmethod
    def delete_category(category_id):
        category = Category.query.get(category_id)
        if not category:
            return jsonify({"error": "Category not found"}), 404

        if category.children:
            return jsonify(
                {"error": "Cannot delete category with child categories"}
            ), 400

        db.session.delete(category)
        db.session.commit()

        return jsonify({"message": "Category deleted successfully"})

    @staticmethod
    def get_categories_by_business(business_id):
        business = Business.query.get(business_id)
        if not business:
            return jsonify({"error": "Business not found"}), 404

        categories = Category.query.filter_by(business_id=business_id).all()
        return jsonify(
            [
                {
                    "id": category.id,
                    "business_id": category.business_id,
                    "name": category.name,
                    "type": category.type,
                    "parent_id": category.parent_id,
                    "created_at": category.created_at.isoformat()
                    if category.created_at
                    else None,
                }
                for category in categories
            ]
        )

    @staticmethod
    def get_root_categories(business_id):
        business = Business.query.get(business_id)
        if not business:
            return jsonify({"error": "Business not found"}), 404

        categories = Category.query.filter_by(
            business_id=business_id, parent_id=None
        ).all()
        return jsonify(
            [
                {
                    "id": category.id,
                    "business_id": category.business_id,
                    "name": category.name,
                    "type": category.type,
                    "parent_id": category.parent_id,
                    "created_at": category.created_at.isoformat()
                    if category.created_at
                    else None,
                }
                for category in categories
            ]
        )

    @staticmethod
    def get_child_categories(parent_id):
        parent = Category.query.get(parent_id)
        if not parent:
            return jsonify({"error": "Parent category not found"}), 404

        categories = Category.query.filter_by(parent_id=parent_id).all()
        return jsonify(
            [
                {
                    "id": category.id,
                    "business_id": category.business_id,
                    "name": category.name,
                    "type": category.type,
                    "parent_id": category.parent_id,
                    "created_at": category.created_at.isoformat()
                    if category.created_at
                    else None,
                }
                for category in categories
            ]
        )
