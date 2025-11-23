from flask import Blueprint
from controllers.transaction_controller import TransactionController

transaction_bp = Blueprint("transactions", __name__)


@transaction_bp.route("/", methods=["POST"])
def create_transaction():
    return TransactionController.create_transaction()


@transaction_bp.route("/", methods=["GET"])
def get_transactions():
    return TransactionController.get_transactions()


@transaction_bp.route("/<int:transaction_id>", methods=["GET"])
def get_transaction(transaction_id):
    return TransactionController.get_transaction(transaction_id)


@transaction_bp.route("/<int:transaction_id>", methods=["PUT"])
def update_transaction(transaction_id):
    return TransactionController.update_transaction(transaction_id)


@transaction_bp.route("/<int:transaction_id>", methods=["DELETE"])
def delete_transaction(transaction_id):
    return TransactionController.delete_transaction(transaction_id)
