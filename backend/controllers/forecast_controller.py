from flask import request, jsonify
from models import db, Forecast, Business, Model, ModelRun, Transaction
from datetime import datetime, date
from decimal import Decimal
from services.ai_service import AIService


class ForecastController:
    @staticmethod
    def create_forecast():
        data = request.get_json()

        required_fields = ["business_id", "granularity", "period_start", "period_end"]
        if not data or not all(field in data for field in required_fields):
            return jsonify(
                {
                    "error": "business_id, granularity, period_start, and period_end are required"
                }
            ), 400

        business = Business.query.get(data["business_id"])
        if not business:
            return jsonify({"error": "Business not found"}), 404

        if "model_id" in data and data["model_id"]:
            model = Model.query.get(data["model_id"])
            if not model:
                return jsonify({"error": "Model not found"}), 404

        if "model_run_id" in data and data["model_run_id"]:
            model_run = ModelRun.query.get(data["model_run_id"])
            if not model_run:
                return jsonify({"error": "Model run not found"}), 404

        period_start = data["period_start"]
        if isinstance(period_start, str):
            period_start = datetime.fromisoformat(period_start).date()

        period_end = data["period_end"]
        if isinstance(period_end, str):
            period_end = datetime.fromisoformat(period_end).date()

        # Initialize metadata if not present
        metadata = data.get("forecast_metadata") or {}

        # Get transactions within the forecast period
        transactions = Transaction.query.filter(
            Transaction.business_id == data["business_id"],
            Transaction.date >= period_start,
            Transaction.date <= period_end,
        ).all()

        # Generate AI Insight
        try:
            ai_service = AIService()
            # Prepare data for AI analysis
            analysis_input = {
                "period_start": period_start,
                "period_end": period_end,
                "granularity": data["granularity"],
                "predicted_value": data.get("predicted_value"),
                "lower_bound": data.get("lower_bound"),
                "upper_bound": data.get("upper_bound"),
                "transactions": [
                    {
                        "date": transaction.date.isoformat(),
                        "amount": float(transaction.amount),
                        "direction": transaction.direction,
                        "description": transaction.description,
                        "category": transaction.category.name
                        if transaction.category
                        else None,
                    }
                    for transaction in transactions
                ],
            }

            insight = ai_service.generate_forecast_insight(analysis_input)
            metadata["ai_analysis"] = insight
            metadata["transaction_count"] = len(transactions)
        except Exception as e:
            print(f"AI Integration Error: {e}")
            metadata["ai_error"] = str(e)
            metadata["transaction_count"] = len(transactions)

        forecast = Forecast(
            business_id=data["business_id"],
            model_run_id=data.get("model_run_id"),
            model_id=data.get("model_id"),
            granularity=data["granularity"],
            period_start=period_start,
            period_end=period_end,
            predicted_value=Decimal(str(data["predicted_value"]))
            if data.get("predicted_value")
            else None,
            lower_bound=Decimal(str(data["lower_bound"]))
            if data.get("lower_bound")
            else None,
            upper_bound=Decimal(str(data["upper_bound"]))
            if data.get("upper_bound")
            else None,
            forecast_metadata=metadata,
        )

        db.session.add(forecast)
        db.session.commit()

        return jsonify(
            {
                "id": forecast.id,
                "business_id": forecast.business_id,
                "model_run_id": forecast.model_run_id,
                "model_id": forecast.model_id,
                "created_at": forecast.created_at.isoformat()
                if forecast.created_at
                else None,
                "granularity": forecast.granularity,
                "period_start": forecast.period_start.isoformat()
                if forecast.period_start
                else None,
                "period_end": forecast.period_end.isoformat()
                if forecast.period_end
                else None,
                "predicted_value": float(forecast.predicted_value)
                if forecast.predicted_value
                else None,
                "lower_bound": float(forecast.lower_bound)
                if forecast.lower_bound
                else None,
                "upper_bound": float(forecast.upper_bound)
                if forecast.upper_bound
                else None,
                "forecast_metadata": forecast.forecast_metadata,
            }
        ), 201

    @staticmethod
    def get_forecasts():
        forecasts = Forecast.query.all()
        return jsonify(
            [
                {
                    "id": forecast.id,
                    "business_id": forecast.business_id,
                    "model_run_id": forecast.model_run_id,
                    "model_id": forecast.model_id,
                    "created_at": forecast.created_at.isoformat()
                    if forecast.created_at
                    else None,
                    "granularity": forecast.granularity,
                    "period_start": forecast.period_start.isoformat()
                    if forecast.period_start
                    else None,
                    "period_end": forecast.period_end.isoformat()
                    if forecast.period_end
                    else None,
                    "predicted_value": float(forecast.predicted_value)
                    if forecast.predicted_value
                    else None,
                    "lower_bound": float(forecast.lower_bound)
                    if forecast.lower_bound
                    else None,
                    "upper_bound": float(forecast.upper_bound)
                    if forecast.upper_bound
                    else None,
                    "forecast_metadata": forecast.forecast_metadata,
                }
                for forecast in forecasts
            ]
        )

    @staticmethod
    def get_forecast(forecast_id):
        forecast = Forecast.query.get(forecast_id)
        if not forecast:
            return jsonify({"error": "Forecast not found"}), 404

        return jsonify(
            {
                "id": forecast.id,
                "business_id": forecast.business_id,
                "model_run_id": forecast.model_run_id,
                "model_id": forecast.model_id,
                "created_at": forecast.created_at.isoformat()
                if forecast.created_at
                else None,
                "granularity": forecast.granularity,
                "period_start": forecast.period_start.isoformat()
                if forecast.period_start
                else None,
                "period_end": forecast.period_end.isoformat()
                if forecast.period_end
                else None,
                "predicted_value": float(forecast.predicted_value)
                if forecast.predicted_value
                else None,
                "lower_bound": float(forecast.lower_bound)
                if forecast.lower_bound
                else None,
                "upper_bound": float(forecast.upper_bound)
                if forecast.upper_bound
                else None,
                "forecast_metadata": forecast.forecast_metadata,
            }
        )

    @staticmethod
    def update_forecast(forecast_id):
        forecast = Forecast.query.get(forecast_id)
        if not forecast:
            return jsonify({"error": "Forecast not found"}), 404

        data = request.get_json()

        if "business_id" in data:
            business = Business.query.get(data["business_id"])
            if not business:
                return jsonify({"error": "Business not found"}), 404
            forecast.business_id = data["business_id"]

        if "model_run_id" in data:
            if data["model_run_id"]:
                model_run = ModelRun.query.get(data["model_run_id"])
                if not model_run:
                    return jsonify({"error": "Model run not found"}), 404
            forecast.model_run_id = data["model_run_id"]

        if "model_id" in data:
            if data["model_id"]:
                model = Model.query.get(data["model_id"])
                if not model:
                    return jsonify({"error": "Model not found"}), 404
            forecast.model_id = data["model_id"]

        if "granularity" in data:
            forecast.granularity = data["granularity"]

        if "period_start" in data:
            period_start = data["period_start"]
            if isinstance(period_start, str):
                period_start = datetime.fromisoformat(period_start).date()
            forecast.period_start = period_start

        if "period_end" in data:
            period_end = data["period_end"]
            if isinstance(period_end, str):
                period_end = datetime.fromisoformat(period_end).date()
            forecast.period_end = period_end

        if "predicted_value" in data:
            forecast.predicted_value = (
                Decimal(str(data["predicted_value"]))
                if data["predicted_value"]
                else None
            )

        if "lower_bound" in data:
            forecast.lower_bound = (
                Decimal(str(data["lower_bound"])) if data["lower_bound"] else None
            )

        if "upper_bound" in data:
            forecast.upper_bound = (
                Decimal(str(data["upper_bound"])) if data["upper_bound"] else None
            )

        if "forecast_metadata" in data:
            forecast.forecast_metadata = data["forecast_metadata"]

        db.session.commit()

        return jsonify(
            {
                "id": forecast.id,
                "business_id": forecast.business_id,
                "model_run_id": forecast.model_run_id,
                "model_id": forecast.model_id,
                "created_at": forecast.created_at.isoformat()
                if forecast.created_at
                else None,
                "granularity": forecast.granularity,
                "period_start": forecast.period_start.isoformat()
                if forecast.period_start
                else None,
                "period_end": forecast.period_end.isoformat()
                if forecast.period_end
                else None,
                "predicted_value": float(forecast.predicted_value)
                if forecast.predicted_value
                else None,
                "lower_bound": float(forecast.lower_bound)
                if forecast.lower_bound
                else None,
                "upper_bound": float(forecast.upper_bound)
                if forecast.upper_bound
                else None,
                "forecast_metadata": forecast.forecast_metadata,
            }
        )

    @staticmethod
    def delete_forecast(forecast_id):
        forecast = Forecast.query.get(forecast_id)
        if not forecast:
            return jsonify({"error": "Forecast not found"}), 404

        db.session.delete(forecast)
        db.session.commit()

        return jsonify({"message": "Forecast deleted successfully"})

    @staticmethod
    def get_forecasts_by_business(business_id):
        business = Business.query.get(business_id)
        if not business:
            return jsonify({"error": "Business not found"}), 404

        forecasts = Forecast.query.filter_by(business_id=business_id).all()
        return jsonify(
            [
                {
                    "id": forecast.id,
                    "business_id": forecast.business_id,
                    "model_run_id": forecast.model_run_id,
                    "model_id": forecast.model_id,
                    "created_at": forecast.created_at.isoformat()
                    if forecast.created_at
                    else None,
                    "granularity": forecast.granularity,
                    "period_start": forecast.period_start.isoformat()
                    if forecast.period_start
                    else None,
                    "period_end": forecast.period_end.isoformat()
                    if forecast.period_end
                    else None,
                    "predicted_value": float(forecast.predicted_value)
                    if forecast.predicted_value
                    else None,
                    "lower_bound": float(forecast.lower_bound)
                    if forecast.lower_bound
                    else None,
                    "upper_bound": float(forecast.upper_bound)
                    if forecast.upper_bound
                    else None,
                    "forecast_metadata": forecast.forecast_metadata,
                }
                for forecast in forecasts
            ]
        )

    @staticmethod
    def get_forecasts_by_model(model_id):
        model = Model.query.get(model_id)
        if not model:
            return jsonify({"error": "Model not found"}), 404

        forecasts = Forecast.query.filter_by(model_id=model_id).all()
        return jsonify(
            [
                {
                    "id": forecast.id,
                    "business_id": forecast.business_id,
                    "model_run_id": forecast.model_run_id,
                    "model_id": forecast.model_id,
                    "created_at": forecast.created_at.isoformat()
                    if forecast.created_at
                    else None,
                    "granularity": forecast.granularity,
                    "period_start": forecast.period_start.isoformat()
                    if forecast.period_start
                    else None,
                    "period_end": forecast.period_end.isoformat()
                    if forecast.period_end
                    else None,
                    "predicted_value": float(forecast.predicted_value)
                    if forecast.predicted_value
                    else None,
                    "lower_bound": float(forecast.lower_bound)
                    if forecast.lower_bound
                    else None,
                    "upper_bound": float(forecast.upper_bound)
                    if forecast.upper_bound
                    else None,
                    "forecast_metadata": forecast.forecast_metadata,
                }
                for forecast in forecasts
            ]
        )
