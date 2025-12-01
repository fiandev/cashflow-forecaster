from flask import Blueprint
from controllers.alert_controller import AlertController
from middleware.auth import authenticate_request
from middleware.permissions import require_role

alert_bp = Blueprint("alerts", __name__)


@alert_bp.route("/", methods=["POST"])
@authenticate_request
@require_role("admin")
def create_alert():
    return AlertController.create_alert()

@alert_bp.route("/", methods=["GET"])
@authenticate_request
def get_alerts():
    return AlertController.get_alerts()


@alert_bp.route("/<int:alert_id>", methods=["GET"])
@authenticate_request
def get_alert(alert_id):
    return AlertController.get_alert(alert_id)


@alert_bp.route("/<int:alert_id>", methods=["PUT"])
@authenticate_request
@require_role("admin")
def update_alert(alert_id):
    return AlertController.update_alert(alert_id)


@alert_bp.route("/<int:alert_id>", methods=["DELETE"])
@authenticate_request
@require_role("admin")
def delete_alert(alert_id):
    return AlertController.delete_alert(alert_id)
