from flask import Blueprint
from controllers.dashboard_controller import DashboardController
from middleware.auth import authenticate_request

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/metrics", methods=["GET"])
@authenticate_request
def get_dashboard_metrics():
    return DashboardController.get_metrics()
