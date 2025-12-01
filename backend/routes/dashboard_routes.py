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
