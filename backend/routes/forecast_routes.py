from middleware.permissions import business_owner_or_admin_required
from flask import Blueprint
from controllers.forecast_controller import ForecastController
from middleware import authenticate_request

forecast_bp = Blueprint("forecasts", __name__)


@forecast_bp.route("/", methods=["POST"])
@authenticate_request
def create_forecast():
    return ForecastController.create_forecast()

@forecast_bp.route("/", methods=["GET"])
@authenticate_request
@business_owner_or_admin_required
def get_forecasts():
    return ForecastController.get_forecasts()

@authenticate_request
@business_owner_or_admin_required
@forecast_bp.route("/<int:forecast_id>", methods=["GET"])
def get_forecast(forecast_id):
    return ForecastController.get_forecast(forecast_id)

@authenticate_request
@business_owner_or_admin_required
@forecast_bp.route("/<int:forecast_id>", methods=["PUT"])
def update_forecast(forecast_id):
    return ForecastController.update_forecast(forecast_id)

@authenticate_request
@business_owner_or_admin_required
@forecast_bp.route("/<int:forecast_id>", methods=["DELETE"])
def delete_forecast(forecast_id):
    return ForecastController.delete_forecast(forecast_id)

@forecast_bp.route("/llm", methods=["POST"])
@authenticate_request
def create_forecast_with_llm():
    return ForecastController.create_forecast_with_llm()
