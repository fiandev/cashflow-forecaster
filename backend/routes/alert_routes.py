from flask import Blueprint
from controllers.alert_controller import AlertController

alert_bp = Blueprint("alerts", __name__)


@alert_bp.route("/", methods=["POST"])
def create_alert():
    return AlertController.create_alert()


@alert_bp.route("/", methods=["GET"])
def get_alerts():
    return AlertController.get_alerts()


@alert_bp.route("/<int:alert_id>", methods=["GET"])
def get_alert(alert_id):
    return AlertController.get_alert(alert_id)


@alert_bp.route("/<int:alert_id>", methods=["PUT"])
def update_alert(alert_id):
    return AlertController.update_alert(alert_id)


@alert_bp.route("/<int:alert_id>", methods=["DELETE"])
def delete_alert(alert_id):
    return AlertController.delete_alert(alert_id)
