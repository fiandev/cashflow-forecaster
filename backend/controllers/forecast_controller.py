from flask import request, jsonify, g
from models import db, Forecast, Business, Model, ModelRun
from datetime import datetime, date
from decimal import Decimal
from services.gemini_forecast_service import GeminiForecastService


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

        # Verify that the current user owns this business or is an admin
        if business.owner_id != g.current_user.id and g.current_user.role != "admin":
            return jsonify({"error": "You don't have permission to create forecasts for this business"}), 403

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

        # Check if LLM should be used (when no predicted values are provided)
        if not data.get("predicted_value") or not data.get("lower_bound") or not data.get("upper_bound"):
            try:
                # Initialize the Gemini forecast service
                gemini_service = GeminiForecastService()

                # Generate forecast using LLM
                forecast_result = gemini_service.generate_forecast_with_gemini(
                    business_id=data["business_id"],
                    period_start=period_start,
                    period_end=period_end,
                    granularity=data["granularity"]
                )

                # Use LLM-generated values
                predicted_value = forecast_result.get('predicted_value')
                lower_bound = forecast_result.get('lower_bound')
                upper_bound = forecast_result.get('upper_bound')

                # Merge forecast metadata
                llm_metadata = {
                    'explanation': forecast_result.get('explanation'),
                    'risk_factors': forecast_result.get('risk_factors'),
                    'confidence_score': forecast_result.get('confidence_score'),
                    'generated_by': 'gemini_llm'
                }

                if data.get("forecast_metadata"):
                    # Merge with existing metadata
                    if isinstance(data["forecast_metadata"], dict):
                        forecast_metadata = {**data["forecast_metadata"], **llm_metadata}
                    else:
                        forecast_metadata = llm_metadata
                else:
                    forecast_metadata = llm_metadata
            except Exception as e:
                return jsonify({"error": f"Error generating forecast with LLM: {str(e)}"}), 500
        else:
            # Use provided values
            predicted_value = Decimal(str(data["predicted_value"])) if data.get("predicted_value") else None
            lower_bound = Decimal(str(data["lower_bound"])) if data.get("lower_bound") else None
            upper_bound = Decimal(str(data["upper_bound"])) if data.get("upper_bound") else None
            forecast_metadata = data.get("forecast_metadata")

        forecast = Forecast(
            business_id=data["business_id"],
            model_run_id=data.get("model_run_id"),
            model_id=data.get("model_id"),
            granularity=data["granularity"],
            period_start=period_start,
            period_end=period_end,
            predicted_value=predicted_value,
            lower_bound=lower_bound,
            upper_bound=upper_bound,
            forecast_metadata=forecast_metadata,
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
    def create_forecast_with_llm():
        """Generate a forecast using Gemini LLM based on business data, transactions, and previous forecasts"""
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

        # Verify that the current user owns this business or is an admin
        if business.owner_id != g.current_user.id and g.current_user.role != "admin":
            return jsonify({"error": "You don't have permission to create forecasts for this business"}), 403

        # Convert period dates if they are strings
        period_start = data["period_start"]
        if isinstance(period_start, str):
            period_start = datetime.fromisoformat(period_start).date()

        period_end = data["period_end"]
        if isinstance(period_end, str):
            period_end = datetime.fromisoformat(period_end).date()

        try:
            # Initialize the Gemini forecast service
            gemini_service = GeminiForecastService()

            # Generate forecast using LLM
            forecast_result = gemini_service.generate_forecast_with_gemini(
                business_id=data["business_id"],
                period_start=period_start,
                period_end=period_end,
                granularity=data["granularity"]
            )

            # Create a new forecast record
            forecast = Forecast(
                business_id=data["business_id"],
                model_run_id=data.get("model_run_id"),
                model_id=data.get("model_id"),
                granularity=data["granularity"],
                period_start=period_start,
                period_end=period_end,
                predicted_value=forecast_result.get('predicted_value'),
                lower_bound=forecast_result.get('lower_bound'),
                upper_bound=forecast_result.get('upper_bound'),
                forecast_metadata={
                    'explanation': forecast_result.get('explanation'),
                    'risk_factors': forecast_result.get('risk_factors'),
                    'confidence_score': forecast_result.get('confidence_score'),
                    'generated_by': 'gemini_llm'
                }
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

        except Exception as e:
            return jsonify({"error": f"Error generating forecast with LLM: {str(e)}"}), 500

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
