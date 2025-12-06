from flask import request, jsonify
from models import db, Model, Business
from datetime import datetime


class ModelController:
    @staticmethod
    def create_model():
        data = request.get_json()

        if not data or not data.get("name") or not data.get("model_type"):
            return jsonify({"error": "Name and model_type are required"}), 400

        if "business_id" in data and data["business_id"]:
            business = Business.query.get(data["business_id"])
            if not business:
                return jsonify({"error": "Business not found"}), 404

        model = Model(
            business_id=data.get("business_id"),
            name=data["name"],
            model_type=data["model_type"],
            params=data.get("params"),
            version=data.get("version"),
            last_trained_at=datetime.fromisoformat(data["last_trained_at"])
            if data.get("last_trained_at")
            else None,
        )

        db.session.add(model)
        db.session.commit()

        return jsonify(
            {
                "id": model.id,
                "business_id": model.business_id,
                "name": model.name,
                "model_type": model.model_type,
                "params": model.params,
                "version": model.version,
                "last_trained_at": model.last_trained_at.isoformat()
                if model.last_trained_at
                else None,
                "created_at": model.created_at.isoformat()
                if model.created_at
                else None,
            }
        ), 201

    @staticmethod
    def get_models():
        models = Model.query.all()
        return jsonify(
            [
                {
                    "id": model.id,
                    "business_id": model.business_id,
                    "name": model.name,
                    "model_type": model.model_type,
                    "params": model.params,
                    "version": model.version,
                    "last_trained_at": model.last_trained_at.isoformat()
                    if model.last_trained_at
                    else None,
                    "created_at": model.created_at.isoformat()
                    if model.created_at
                    else None,
                }
                for model in models
            ]
        )

    @staticmethod
    def get_model(model_id):
        model = Model.query.get(model_id)
        if not model:
            return jsonify({"error": "Model not found"}), 404

        return jsonify(
            {
                "id": model.id,
                "business_id": model.business_id,
                "name": model.name,
                "model_type": model.model_type,
                "params": model.params,
                "version": model.version,
                "last_trained_at": model.last_trained_at.isoformat()
                if model.last_trained_at
                else None,
                "created_at": model.created_at.isoformat()
                if model.created_at
                else None,
            }
        )

    @staticmethod
    def update_model(model_id):
        model = Model.query.get(model_id)
        if not model:
            return jsonify({"error": "Model not found"}), 404

        data = request.get_json()

        if "business_id" in data:
            if data["business_id"]:
                business = Business.query.get(data["business_id"])
                if not business:
                    return jsonify({"error": "Business not found"}), 404
            model.business_id = data["business_id"]

        if "name" in data:
            model.name = data["name"]

        if "model_type" in data:
            model.model_type = data["model_type"]

        if "params" in data:
            model.params = data["params"]

        if "version" in data:
            model.version = data["version"]

        if "last_trained_at" in data:
            model.last_trained_at = (
                datetime.fromisoformat(data["last_trained_at"])
                if data["last_trained_at"]
                else None
            )

        db.session.commit()

        return jsonify(
            {
                "id": model.id,
                "business_id": model.business_id,
                "name": model.name,
                "model_type": model.model_type,
                "params": model.params,
                "version": model.version,
                "last_trained_at": model.last_trained_at.isoformat()
                if model.last_trained_at
                else None,
                "created_at": model.created_at.isoformat()
                if model.created_at
                else None,
            }
        )

    @staticmethod
    def delete_model(model_id):
        model = Model.query.get(model_id)
        if not model:
            return jsonify({"error": "Model not found"}), 404

        db.session.delete(model)
        db.session.commit()

        return jsonify({"message": "Model deleted successfully"})

    @staticmethod
    def get_models_by_business(business_id):
        business = Business.query.get(business_id)
        if not business:
            return jsonify({"error": "Business not found"}), 404

        models = Model.query.filter_by(business_id=business_id).all()
        return jsonify(
            [
                {
                    "id": model.id,
                    "business_id": model.business_id,
                    "name": model.name,
                    "model_type": model.model_type,
                    "params": model.params,
                    "version": model.version,
                    "last_trained_at": model.last_trained_at.isoformat()
                    if model.last_trained_at
                    else None,
                    "created_at": model.created_at.isoformat()
                    if model.created_at
                    else None,
                }
                for model in models
            ]
        )

    @staticmethod
    def get_models_by_type(model_type):
        models = Model.query.filter_by(model_type=model_type).all()
        return jsonify(
            [
                {
                    "id": model.id,
                    "business_id": model.business_id,
                    "name": model.name,
                    "model_type": model.model_type,
                    "params": model.params,
                    "version": model.version,
                    "last_trained_at": model.last_trained_at.isoformat()
                    if model.last_trained_at
                    else None,
                    "created_at": model.created_at.isoformat()
                    if model.created_at
                    else None,
                }
                for model in models
            ]
        )
