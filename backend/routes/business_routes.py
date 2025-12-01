from flask import Blueprint
from controllers.business_controller import BusinessController

business_controller = BusinessController()
business_bp = Blueprint("businesses", __name__)


@business_bp.route("/", methods=["GET"])
def get_businesses():
    return business_controller.get_businesses()


@business_bp.route("/<int:business_id>", methods=["GET"])
def get_business(business_id):
    return business_controller.get_business(business_id)


@business_bp.route("/<int:business_id>", methods=["PUT"])
def update_business(business_id):
    return business_controller.update_business(business_id)


@business_bp.route("/<int:business_id>", methods=["DELETE"])
def delete_business(business_id):
    return business_controller.delete_business(business_id)
