from flask import request, jsonify
from models import db, Alert, Business, Transaction, Forecast
from datetime import datetime


class AlertController:
    @staticmethod
    def create_alert():
        data = request.get_json()

        if (
            not data
            or not data.get("business_id")
            or not data.get("level")
            or not data.get("message")
        ):
            return jsonify(
                {"error": "business_id, level, and message are required"}
            ), 400

        business = Business.query.get(data["business_id"])
        if not business:
            return jsonify({"error": "Business not found"}), 404

        if "linked_transaction_id" in data and data["linked_transaction_id"]:
            transaction = Transaction.query.get(data["linked_transaction_id"])
            if not transaction:
                return jsonify({"error": "Transaction not found"}), 404

        if "linked_forecast_id" in data and data["linked_forecast_id"]:
            forecast = Forecast.query.get(data["linked_forecast_id"])
            if not forecast:
                return jsonify({"error": "Forecast not found"}), 404

        alert = Alert(
            business_id=data["business_id"],
            level=data["level"],
            message=data["message"],
            linked_transaction_id=data.get("linked_transaction_id"),
            linked_forecast_id=data.get("linked_forecast_id"),
            resolved=data.get("resolved", False),
            resolved_at=datetime.fromisoformat(data["resolved_at"])
            if data.get("resolved_at")
            else None,
            forecast_metadata=data.get("forecast_metadata"),
        )

        db.session.add(alert)
        db.session.commit()

        return jsonify(
            {
                "id": alert.id,
                "business_id": alert.business_id,
                "created_at": alert.created_at.isoformat()
                if alert.created_at
                else None,
                "level": alert.level,
                "message": alert.message,
                "linked_transaction_id": alert.linked_transaction_id,
                "linked_forecast_id": alert.linked_forecast_id,
                "resolved": alert.resolved,
                "resolved_at": alert.resolved_at.isoformat()
                if alert.resolved_at
                else None,
                "forecast_metadata": alert.forecast_metadata,
            }
        ), 201

    @staticmethod
    def get_alerts():
        alerts = Alert.query.all()
        return jsonify(
            [
                {
                    "id": alert.id,
                    "business_id": alert.business_id,
                    "created_at": alert.created_at.isoformat()
                    if alert.created_at
                    else None,
                    "level": alert.level,
                    "message": alert.message,
                    "linked_transaction_id": alert.linked_transaction_id,
                    "linked_forecast_id": alert.linked_forecast_id,
                    "resolved": alert.resolved,
                    "resolved_at": alert.resolved_at.isoformat()
                    if alert.resolved_at
                    else None,
                    "forecast_metadata": alert.forecast_metadata,
                }
                for alert in alerts
            ]
        )

    @staticmethod
    def get_alert(alert_id):
        alert = Alert.query.get(alert_id)
        if not alert:
            return jsonify({"error": "Alert not found"}), 404

        return jsonify(
            {
                "id": alert.id,
                "business_id": alert.business_id,
                "created_at": alert.created_at.isoformat()
                if alert.created_at
                else None,
                "level": alert.level,
                "message": alert.message,
                "linked_transaction_id": alert.linked_transaction_id,
                "linked_forecast_id": alert.linked_forecast_id,
                "resolved": alert.resolved,
                "resolved_at": alert.resolved_at.isoformat()
                if alert.resolved_at
                else None,
                "forecast_metadata": alert.forecast_metadata,
            }
        )

    @staticmethod
    def update_alert(alert_id):
        alert = Alert.query.get(alert_id)
        if not alert:
            return jsonify({"error": "Alert not found"}), 404

        data = request.get_json()

        if "business_id" in data:
            business = Business.query.get(data["business_id"])
            if not business:
                return jsonify({"error": "Business not found"}), 404
            alert.business_id = data["business_id"]

        if "level" in data:
            alert.level = data["level"]

        if "message" in data:
            alert.message = data["message"]

        if "linked_transaction_id" in data:
            if data["linked_transaction_id"]:
                transaction = Transaction.query.get(data["linked_transaction_id"])
                if not transaction:
                    return jsonify({"error": "Transaction not found"}), 404
            alert.linked_transaction_id = data["linked_transaction_id"]

        if "linked_forecast_id" in data:
            if data["linked_forecast_id"]:
                forecast = Forecast.query.get(data["linked_forecast_id"])
                if not forecast:
                    return jsonify({"error": "Forecast not found"}), 404
            alert.linked_forecast_id = data["linked_forecast_id"]

        if "resolved" in data:
            alert.resolved = data["resolved"]
            if data["resolved"] and not alert.resolved_at:
                alert.resolved_at = datetime.utcnow()
            elif not data["resolved"]:
                alert.resolved_at = None

        if "resolved_at" in data:
            alert.resolved_at = (
                datetime.fromisoformat(data["resolved_at"])
                if data["resolved_at"]
                else None
            )

        if "forecast_metadata" in data:
            alert.forecast_metadata = data["forecast_metadata"]

        db.session.commit()

        return jsonify(
            {
                "id": alert.id,
                "business_id": alert.business_id,
                "created_at": alert.created_at.isoformat()
                if alert.created_at
                else None,
                "level": alert.level,
                "message": alert.message,
                "linked_transaction_id": alert.linked_transaction_id,
                "linked_forecast_id": alert.linked_forecast_id,
                "resolved": alert.resolved,
                "resolved_at": alert.resolved_at.isoformat()
                if alert.resolved_at
                else None,
                "forecast_metadata": alert.forecast_metadata,
            }
        )

    @staticmethod
    def delete_alert(alert_id):
        alert = Alert.query.get(alert_id)
        if not alert:
            return jsonify({"error": "Alert not found"}), 404

        db.session.delete(alert)
        db.session.commit()

        return jsonify({"message": "Alert deleted successfully"})

    @staticmethod
    def get_alerts_by_business(business_id):
        business = Business.query.get(business_id)
        if not business:
            return jsonify({"error": "Business not found"}), 404

        alerts = Alert.query.filter_by(business_id=business_id).all()
        return jsonify(
            [
                {
                    "id": alert.id,
                    "business_id": alert.business_id,
                    "created_at": alert.created_at.isoformat()
                    if alert.created_at
                    else None,
                    "level": alert.level,
                    "message": alert.message,
                    "linked_transaction_id": alert.linked_transaction_id,
                    "linked_forecast_id": alert.linked_forecast_id,
                    "resolved": alert.resolved,
                    "resolved_at": alert.resolved_at.isoformat()
                    if alert.resolved_at
                    else None,
                    "forecast_metadata": alert.forecast_metadata,
                }
                for alert in alerts
            ]
        )

    @staticmethod
    def get_alerts_by_level(level):
        alerts = Alert.query.filter_by(level=level).all()
        return jsonify(
            [
                {
                    "id": alert.id,
                    "business_id": alert.business_id,
                    "created_at": alert.created_at.isoformat()
                    if alert.created_at
                    else None,
                    "level": alert.level,
                    "message": alert.message,
                    "linked_transaction_id": alert.linked_transaction_id,
                    "linked_forecast_id": alert.linked_forecast_id,
                    "resolved": alert.resolved,
                    "resolved_at": alert.resolved_at.isoformat()
                    if alert.resolved_at
                    else None,
                    "forecast_metadata": alert.forecast_metadata,
                }
                for alert in alerts
            ]
        )

    @staticmethod
    def get_unresolved_alerts():
        alerts = Alert.query.filter_by(resolved=False).all()
        return jsonify(
            [
                {
                    "id": alert.id,
                    "business_id": alert.business_id,
                    "created_at": alert.created_at.isoformat()
                    if alert.created_at
                    else None,
                    "level": alert.level,
                    "message": alert.message,
                    "linked_transaction_id": alert.linked_transaction_id,
                    "linked_forecast_id": alert.linked_forecast_id,
                    "resolved": alert.resolved,
                    "resolved_at": alert.resolved_at.isoformat()
                    if alert.resolved_at
                    else None,
                    "forecast_metadata": alert.forecast_metadata,
                }
                for alert in alerts
            ]
        )

    @staticmethod
    def resolve_alert(alert_id):
        alert = Alert.query.get(alert_id)
        if not alert:
            return jsonify({"error": "Alert not found"}), 404

        alert.resolved = True
        alert.resolved_at = datetime.utcnow()
        db.session.commit()

        return jsonify(
            {
                "id": alert.id,
                "business_id": alert.business_id,
                "created_at": alert.created_at.isoformat()
                if alert.created_at
                else None,
                "level": alert.level,
                "message": alert.message,
                "linked_transaction_id": alert.linked_transaction_id,
                "linked_forecast_id": alert.linked_forecast_id,
                "resolved": alert.resolved,
                "resolved_at": alert.resolved_at.isoformat()
                if alert.resolved_at
                else None,
                "forecast_metadata": alert.forecast_metadata,
            }
        )
