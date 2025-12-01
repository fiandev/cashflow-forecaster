from flask import Blueprint
from controllers.dashboard_controller import DashboardController
from middleware import authenticate_request, business_owner_required

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/stats/<int:business_id>", methods=["GET"])
@authenticate_request
@business_owner_required
def get_dashboard(business_id):
    """
    Get comprehensive dashboard data
    Requires: business_id as path parameter
    """
    return DashboardController.get_dashboard_data(business_id)


@dashboard_bp.route("/actual-stats-after-forecast/<int:business_id>", methods=["GET"])
@authenticate_request
@business_owner_required
def get_actual_stats_after_forecast(business_id):
    """
    Get actual stats and calculated metrics after forecast
    Requires: business_id as path parameter
    """
    return DashboardController.get_actual_stats_after_forecast(business_id)


@dashboard_bp.route("/generate-ai-alerts/<int:business_id>", methods=["POST"])
@authenticate_request
@business_owner_required
def generate_ai_alerts(business_id):
    """
    Generate AI-powered alerts based on business data
    Requires: business_id as path parameter
    """
    return DashboardController.generate_ai_alerts(business_id)
