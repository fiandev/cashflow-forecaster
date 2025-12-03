from flask import Blueprint
from controllers.category_controller import CategoryController
from middleware.auth import authenticate_request

category_bp = Blueprint("categories", __name__)


@category_bp.route("/", methods=["POST"])
@authenticate_request
def create_category():
    return CategoryController.create_category()


@category_bp.route("/", methods=["GET"])
@authenticate_request
def get_categories():
    return CategoryController.get_categories()


@category_bp.route("/<int:category_id>", methods=["GET"])
@authenticate_request
def get_category(category_id):
    return CategoryController.get_category(category_id)


@category_bp.route("/<int:category_id>", methods=["PUT"])
@authenticate_request
def update_category(category_id):
    return CategoryController.update_category(category_id)


@category_bp.route("/<int:category_id>", methods=["DELETE"])
@authenticate_request
def delete_category(category_id):
    return CategoryController.delete_category(category_id)
