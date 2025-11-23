from flask import request, jsonify
from models import db, Transaction, Business, Category, OCRDocument
from datetime import datetime, date


class TransactionController:
    @staticmethod
    def create_transaction():
        data = request.get_json()

        required_fields = ["business_id", "date", "amount", "direction"]
        if not data or not all(field in data for field in required_fields):
            return jsonify(
                {"error": "business_id, date, amount, and direction are required"}
            ), 400

        business = Business.query.get(data["business_id"])
        if not business:
            return jsonify({"error": "Business not found"}), 404

        if "category_id" in data and data["category_id"]:
            category = Category.query.get(data["category_id"])
            if not category:
                return jsonify({"error": "Category not found"}), 404

        if "ocr_document_id" in data and data["ocr_document_id"]:
            ocr_doc = OCRDocument.query.get(data["ocr_document_id"])
            if not ocr_doc:
                return jsonify({"error": "OCR document not found"}), 404

        transaction_date = data["date"]
        if isinstance(transaction_date, str):
            transaction_date = datetime.fromisoformat(transaction_date).date()

        transaction = Transaction(
            business_id=data["business_id"],
            date=transaction_date,
            datetime=datetime.fromisoformat(data["datetime"])
            if data.get("datetime")
            else None,
            description=data.get("description"),
            amount=data["amount"],
            direction=data["direction"],
            category_id=data.get("category_id"),
            source=data.get("source"),
            ocr_document_id=data.get("ocr_document_id"),
            tags=data.get("tags"),
            is_anomalous=data.get("is_anomalous", False),
            ai_tag=data.get("ai_tag"),
        )

        db.session.add(transaction)
        db.session.commit()

        return jsonify(
            {
                "id": transaction.id,
                "business_id": transaction.business_id,
                "date": transaction.date.isoformat() if transaction.date else None,
                "datetime": transaction.datetime.isoformat()
                if transaction.datetime
                else None,
                "description": transaction.description,
                "amount": float(transaction.amount) if transaction.amount else None,
                "direction": transaction.direction,
                "category_id": transaction.category_id,
                "source": transaction.source,
                "ocr_document_id": transaction.ocr_document_id,
                "tags": transaction.tags,
                "is_anomalous": transaction.is_anomalous,
                "ai_tag": transaction.ai_tag,
                "created_at": transaction.created_at.isoformat()
                if transaction.created_at
                else None,
                "updated_at": transaction.updated_at.isoformat()
                if transaction.updated_at
                else None,
            }
        ), 201

    @staticmethod
    def get_transactions():
        transactions = Transaction.query.all()
        return jsonify(
            [
                {
                    "id": transaction.id,
                    "business_id": transaction.business_id,
                    "date": transaction.date.isoformat() if transaction.date else None,
                    "datetime": transaction.datetime.isoformat()
                    if transaction.datetime
                    else None,
                    "description": transaction.description,
                    "amount": float(transaction.amount) if transaction.amount else None,
                    "direction": transaction.direction,
                    "category_id": transaction.category_id,
                    "source": transaction.source,
                    "ocr_document_id": transaction.ocr_document_id,
                    "tags": transaction.tags,
                    "is_anomalous": transaction.is_anomalous,
                    "ai_tag": transaction.ai_tag,
                    "created_at": transaction.created_at.isoformat()
                    if transaction.created_at
                    else None,
                    "updated_at": transaction.updated_at.isoformat()
                    if transaction.updated_at
                    else None,
                }
                for transaction in transactions
            ]
        )

    @staticmethod
    def get_transaction(transaction_id):
        transaction = Transaction.query.get(transaction_id)
        if not transaction:
            return jsonify({"error": "Transaction not found"}), 404

        return jsonify(
            {
                "id": transaction.id,
                "business_id": transaction.business_id,
                "date": transaction.date.isoformat() if transaction.date else None,
                "datetime": transaction.datetime.isoformat()
                if transaction.datetime
                else None,
                "description": transaction.description,
                "amount": float(transaction.amount) if transaction.amount else None,
                "direction": transaction.direction,
                "category_id": transaction.category_id,
                "source": transaction.source,
                "ocr_document_id": transaction.ocr_document_id,
                "tags": transaction.tags,
                "is_anomalous": transaction.is_anomalous,
                "ai_tag": transaction.ai_tag,
                "created_at": transaction.created_at.isoformat()
                if transaction.created_at
                else None,
                "updated_at": transaction.updated_at.isoformat()
                if transaction.updated_at
                else None,
            }
        )

    @staticmethod
    def update_transaction(transaction_id):
        transaction = Transaction.query.get(transaction_id)
        if not transaction:
            return jsonify({"error": "Transaction not found"}), 404

        data = request.get_json()

        if "business_id" in data:
            business = Business.query.get(data["business_id"])
            if not business:
                return jsonify({"error": "Business not found"}), 404
            transaction.business_id = data["business_id"]

        if "date" in data:
            transaction_date = data["date"]
            if isinstance(transaction_date, str):
                transaction_date = datetime.fromisoformat(transaction_date).date()
            transaction.date = transaction_date

        if "datetime" in data:
            transaction.datetime = (
                datetime.fromisoformat(data["datetime"]) if data["datetime"] else None
            )

        if "description" in data:
            transaction.description = data["description"]

        if "amount" in data:
            transaction.amount = data["amount"]

        if "direction" in data:
            transaction.direction = data["direction"]

        if "category_id" in data:
            if data["category_id"]:
                category = Category.query.get(data["category_id"])
                if not category:
                    return jsonify({"error": "Category not found"}), 404
            transaction.category_id = data["category_id"]

        if "source" in data:
            transaction.source = data["source"]

        if "ocr_document_id" in data:
            if data["ocr_document_id"]:
                ocr_doc = OCRDocument.query.get(data["ocr_document_id"])
                if not ocr_doc:
                    return jsonify({"error": "OCR document not found"}), 404
            transaction.ocr_document_id = data["ocr_document_id"]

        if "tags" in data:
            transaction.tags = data["tags"]

        if "is_anomalous" in data:
            transaction.is_anomalous = data["is_anomalous"]

        if "ai_tag" in data:
            transaction.ai_tag = data["ai_tag"]

        transaction.updated_at = datetime.utcnow()
        db.session.commit()

        return jsonify(
            {
                "id": transaction.id,
                "business_id": transaction.business_id,
                "date": transaction.date.isoformat() if transaction.date else None,
                "datetime": transaction.datetime.isoformat()
                if transaction.datetime
                else None,
                "description": transaction.description,
                "amount": float(transaction.amount) if transaction.amount else None,
                "direction": transaction.direction,
                "category_id": transaction.category_id,
                "source": transaction.source,
                "ocr_document_id": transaction.ocr_document_id,
                "tags": transaction.tags,
                "is_anomalous": transaction.is_anomalous,
                "ai_tag": transaction.ai_tag,
                "created_at": transaction.created_at.isoformat()
                if transaction.created_at
                else None,
                "updated_at": transaction.updated_at.isoformat()
                if transaction.updated_at
                else None,
            }
        )

    @staticmethod
    def delete_transaction(transaction_id):
        transaction = Transaction.query.get(transaction_id)
        if not transaction:
            return jsonify({"error": "Transaction not found"}), 404

        db.session.delete(transaction)
        db.session.commit()

        return jsonify({"message": "Transaction deleted successfully"})

    @staticmethod
    def get_transactions_by_business(business_id):
        business = Business.query.get(business_id)
        if not business:
            return jsonify({"error": "Business not found"}), 404

        transactions = Transaction.query.filter_by(business_id=business_id).all()
        return jsonify(
            [
                {
                    "id": transaction.id,
                    "business_id": transaction.business_id,
                    "date": transaction.date.isoformat() if transaction.date else None,
                    "datetime": transaction.datetime.isoformat()
                    if transaction.datetime
                    else None,
                    "description": transaction.description,
                    "amount": float(transaction.amount) if transaction.amount else None,
                    "direction": transaction.direction,
                    "category_id": transaction.category_id,
                    "source": transaction.source,
                    "ocr_document_id": transaction.ocr_document_id,
                    "tags": transaction.tags,
                    "is_anomalous": transaction.is_anomalous,
                    "ai_tag": transaction.ai_tag,
                    "created_at": transaction.created_at.isoformat()
                    if transaction.created_at
                    else None,
                    "updated_at": transaction.updated_at.isoformat()
                    if transaction.updated_at
                    else None,
                }
                for transaction in transactions
            ]
        )

    @staticmethod
    def get_transactions_by_category(category_id):
        category = Category.query.get(category_id)
        if not category:
            return jsonify({"error": "Category not found"}), 404

        transactions = Transaction.query.filter_by(category_id=category_id).all()
        return jsonify(
            [
                {
                    "id": transaction.id,
                    "business_id": transaction.business_id,
                    "date": transaction.date.isoformat() if transaction.date else None,
                    "datetime": transaction.datetime.isoformat()
                    if transaction.datetime
                    else None,
                    "description": transaction.description,
                    "amount": float(transaction.amount) if transaction.amount else None,
                    "direction": transaction.direction,
                    "category_id": transaction.category_id,
                    "source": transaction.source,
                    "ocr_document_id": transaction.ocr_document_id,
                    "tags": transaction.tags,
                    "is_anomalous": transaction.is_anomalous,
                    "ai_tag": transaction.ai_tag,
                    "created_at": transaction.created_at.isoformat()
                    if transaction.created_at
                    else None,
                    "updated_at": transaction.updated_at.isoformat()
                    if transaction.updated_at
                    else None,
                }
                for transaction in transactions
            ]
        )
