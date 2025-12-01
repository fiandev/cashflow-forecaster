from flask import Blueprint
from controllers.business_controller import BusinessController
from middleware.auth import authenticate_request
from middleware.permissions import business_owner_required, business_owner_or_admin_required

business_controller = BusinessController()
business_bp = Blueprint("businesses", __name__)


@business_bp.route("/", methods=["GET"])
@authenticate_request
def get_businesses():
    return business_controller.get_businesses()


@business_bp.route("/<int:business_id>", methods=["GET"])
@authenticate_request
@business_owner_or_admin_required
def get_business(business_id):
    return business_controller.get_business(business_id)


@business_bp.route("/<int:business_id>", methods=["PUT"])
@authenticate_request
@business_owner_or_admin_required
def update_business(business_id):
    return business_controller.update_business(business_id)


@business_bp.route("/<int:business_id>", methods=["DELETE"])
@authenticate_request
@business_owner_or_admin_required
def delete_business(business_id):
    return business_controller.delete_business(business_id)
