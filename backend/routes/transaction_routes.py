from flask import Blueprint
from controllers.transaction_controller import TransactionController
from middleware import authenticate_request
from middleware.permissions import transaction_access_required

transaction_bp = Blueprint("transactions", __name__)


@transaction_bp.route("/", methods=["POST"])
@authenticate_request
@transaction_access_required
def create_transaction():
    return TransactionController.create_transaction()


@transaction_bp.route("/", methods=["GET"])
@authenticate_request
@transaction_access_required
def get_transactions():
    return TransactionController.get_transactions()


@transaction_bp.route("/<int:transaction_id>", methods=["GET"])
@authenticate_request
@transaction_access_required
def get_transaction(transaction_id):
    return TransactionController.get_transaction(transaction_id)


@transaction_bp.route("/<int:transaction_id>", methods=["PUT"])
@authenticate_request
@transaction_access_required
def update_transaction(transaction_id):
    return TransactionController.update_transaction(transaction_id)


@transaction_bp.route("/<int:transaction_id>", methods=["DELETE"])
@authenticate_request
@transaction_access_required
def delete_transaction(transaction_id):
    return TransactionController.delete_transaction(transaction_id)
