from flask import Blueprint
from controllers.forecast_controller import ForecastController

forecast_bp = Blueprint("forecasts", __name__)


@forecast_bp.route("/", methods=["POST"])
def create_forecast():
    return ForecastController.create_forecast()


@forecast_bp.route("/", methods=["GET"])
def get_forecasts():
    return ForecastController.get_forecasts()


@forecast_bp.route("/<int:forecast_id>", methods=["GET"])
def get_forecast(forecast_id):
    return ForecastController.get_forecast(forecast_id)


@forecast_bp.route("/<int:forecast_id>", methods=["PUT"])
def update_forecast(forecast_id):
    return ForecastController.update_forecast(forecast_id)


@forecast_bp.route("/<int:forecast_id>", methods=["DELETE"])
def delete_forecast(forecast_id):
    return ForecastController.delete_forecast(forecast_id)
