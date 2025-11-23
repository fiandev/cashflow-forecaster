from flask import request, jsonify
from models import db, RiskScore, Business, Forecast
from decimal import Decimal


class RiskScoreController:
    @staticmethod
    def create_risk_score():
        data = request.get_json()

        if not data or not data.get("business_id"):
            return jsonify({"error": "business_id is required"}), 400

        business = Business.query.get(data["business_id"])
        if not business:
            return jsonify({"error": "Business not found"}), 404

        if "source_forecast_id" in data and data["source_forecast_id"]:
            forecast = Forecast.query.get(data["source_forecast_id"])
            if not forecast:
                return jsonify({"error": "Forecast not found"}), 404

        risk_score = RiskScore(
            business_id=data["business_id"],
            liquidity_score=Decimal(str(data["liquidity_score"]))
            if data.get("liquidity_score")
            else None,
            cashflow_risk_score=Decimal(str(data["cashflow_risk_score"]))
            if data.get("cashflow_risk_score")
            else None,
            volatility_index=Decimal(str(data["volatility_index"]))
            if data.get("volatility_index")
            else None,
            drawdown_prob=Decimal(str(data["drawdown_prob"]))
            if data.get("drawdown_prob")
            else None,
            source_forecast_id=data.get("source_forecast_id"),
            details=data.get("details"),
        )

        db.session.add(risk_score)
        db.session.commit()

        return jsonify(
            {
                "id": risk_score.id,
                "business_id": risk_score.business_id,
                "assessed_at": risk_score.assessed_at.isoformat()
                if risk_score.assessed_at
                else None,
                "liquidity_score": float(risk_score.liquidity_score)
                if risk_score.liquidity_score
                else None,
                "cashflow_risk_score": float(risk_score.cashflow_risk_score)
                if risk_score.cashflow_risk_score
                else None,
                "volatility_index": float(risk_score.volatility_index)
                if risk_score.volatility_index
                else None,
                "drawdown_prob": float(risk_score.drawdown_prob)
                if risk_score.drawdown_prob
                else None,
                "source_forecast_id": risk_score.source_forecast_id,
                "details": risk_score.details,
            }
        ), 201

    @staticmethod
    def get_risk_scores():
        risk_scores = RiskScore.query.all()
        return jsonify(
            [
                {
                    "id": score.id,
                    "business_id": score.business_id,
                    "assessed_at": score.assessed_at.isoformat()
                    if score.assessed_at
                    else None,
                    "liquidity_score": float(score.liquidity_score)
                    if score.liquidity_score
                    else None,
                    "cashflow_risk_score": float(score.cashflow_risk_score)
                    if score.cashflow_risk_score
                    else None,
                    "volatility_index": float(score.volatility_index)
                    if score.volatility_index
                    else None,
                    "drawdown_prob": float(score.drawdown_prob)
                    if score.drawdown_prob
                    else None,
                    "source_forecast_id": score.source_forecast_id,
                    "details": score.details,
                }
                for score in risk_scores
            ]
        )

    @staticmethod
    def get_risk_score(risk_score_id):
        risk_score = RiskScore.query.get(risk_score_id)
        if not risk_score:
            return jsonify({"error": "Risk score not found"}), 404

        return jsonify(
            {
                "id": risk_score.id,
                "business_id": risk_score.business_id,
                "assessed_at": risk_score.assessed_at.isoformat()
                if risk_score.assessed_at
                else None,
                "liquidity_score": float(risk_score.liquidity_score)
                if risk_score.liquidity_score
                else None,
                "cashflow_risk_score": float(risk_score.cashflow_risk_score)
                if risk_score.cashflow_risk_score
                else None,
                "volatility_index": float(risk_score.volatility_index)
                if risk_score.volatility_index
                else None,
                "drawdown_prob": float(risk_score.drawdown_prob)
                if risk_score.drawdown_prob
                else None,
                "source_forecast_id": risk_score.source_forecast_id,
                "details": risk_score.details,
            }
        )

    @staticmethod
    def update_risk_score(risk_score_id):
        risk_score = RiskScore.query.get(risk_score_id)
        if not risk_score:
            return jsonify({"error": "Risk score not found"}), 404

        data = request.get_json()

        if "business_id" in data:
            business = Business.query.get(data["business_id"])
            if not business:
                return jsonify({"error": "Business not found"}), 404
            risk_score.business_id = data["business_id"]

        if "liquidity_score" in data:
            risk_score.liquidity_score = (
                Decimal(str(data["liquidity_score"]))
                if data["liquidity_score"]
                else None
            )

        if "cashflow_risk_score" in data:
            risk_score.cashflow_risk_score = (
                Decimal(str(data["cashflow_risk_score"]))
                if data["cashflow_risk_score"]
                else None
            )

        if "volatility_index" in data:
            risk_score.volatility_index = (
                Decimal(str(data["volatility_index"]))
                if data["volatility_index"]
                else None
            )

        if "drawdown_prob" in data:
            risk_score.drawdown_prob = (
                Decimal(str(data["drawdown_prob"])) if data["drawdown_prob"] else None
            )

        if "source_forecast_id" in data:
            if data["source_forecast_id"]:
                forecast = Forecast.query.get(data["source_forecast_id"])
                if not forecast:
                    return jsonify({"error": "Forecast not found"}), 404
            risk_score.source_forecast_id = data["source_forecast_id"]

        if "details" in data:
            risk_score.details = data["details"]

        db.session.commit()

        return jsonify(
            {
                "id": risk_score.id,
                "business_id": risk_score.business_id,
                "assessed_at": risk_score.assessed_at.isoformat()
                if risk_score.assessed_at
                else None,
                "liquidity_score": float(risk_score.liquidity_score)
                if risk_score.liquidity_score
                else None,
                "cashflow_risk_score": float(risk_score.cashflow_risk_score)
                if risk_score.cashflow_risk_score
                else None,
                "volatility_index": float(risk_score.volatility_index)
                if risk_score.volatility_index
                else None,
                "drawdown_prob": float(risk_score.drawdown_prob)
                if risk_score.drawdown_prob
                else None,
                "source_forecast_id": risk_score.source_forecast_id,
                "details": risk_score.details,
            }
        )

    @staticmethod
    def delete_risk_score(risk_score_id):
        risk_score = RiskScore.query.get(risk_score_id)
        if not risk_score:
            return jsonify({"error": "Risk score not found"}), 404

        db.session.delete(risk_score)
        db.session.commit()

        return jsonify({"message": "Risk score deleted successfully"})

    @staticmethod
    def get_risk_scores_by_business(business_id):
        business = Business.query.get(business_id)
        if not business:
            return jsonify({"error": "Business not found"}), 404

        risk_scores = RiskScore.query.filter_by(business_id=business_id).all()
        return jsonify(
            [
                {
                    "id": score.id,
                    "business_id": score.business_id,
                    "assessed_at": score.assessed_at.isoformat()
                    if score.assessed_at
                    else None,
                    "liquidity_score": float(score.liquidity_score)
                    if score.liquidity_score
                    else None,
                    "cashflow_risk_score": float(score.cashflow_risk_score)
                    if score.cashflow_risk_score
                    else None,
                    "volatility_index": float(score.volatility_index)
                    if score.volatility_index
                    else None,
                    "drawdown_prob": float(score.drawdown_prob)
                    if score.drawdown_prob
                    else None,
                    "source_forecast_id": score.source_forecast_id,
                    "details": score.details,
                }
                for score in risk_scores
            ]
        )

    @staticmethod
    def get_risk_scores_by_forecast(forecast_id):
        forecast = Forecast.query.get(forecast_id)
        if not forecast:
            return jsonify({"error": "Forecast not found"}), 404

        risk_scores = RiskScore.query.filter_by(source_forecast_id=forecast_id).all()
        return jsonify(
            [
                {
                    "id": score.id,
                    "business_id": score.business_id,
                    "assessed_at": score.assessed_at.isoformat()
                    if score.assessed_at
                    else None,
                    "liquidity_score": float(score.liquidity_score)
                    if score.liquidity_score
                    else None,
                    "cashflow_risk_score": float(score.cashflow_risk_score)
                    if score.cashflow_risk_score
                    else None,
                    "volatility_index": float(score.volatility_index)
                    if score.volatility_index
                    else None,
                    "drawdown_prob": float(score.drawdown_prob)
                    if score.drawdown_prob
                    else None,
                    "source_forecast_id": score.source_forecast_id,
                    "details": score.details,
                }
                for score in risk_scores
            ]
        )
