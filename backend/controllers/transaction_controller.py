from flask import request, jsonify, g
from models import db, Transaction, Business, Category, OCRDocument, Alert
from datetime import datetime, date
from services.ai_service import AIService
import json


class TransactionController:
    @staticmethod
    def create_transaction():
        data = request.get_json()

        # Verify user is authenticated
        if not hasattr(g, 'current_user') or not g.current_user:
            return jsonify({"error": "Authentication required"}), 401

        # Map 'type' to 'direction' for compatibility
        if 'type' in data and 'direction' not in data:
            # Convert type to direction: 'income' -> 'inflow', 'expense' -> 'outflow'
            transaction_type = data['type'].lower()
            if transaction_type in ['income', 'inflow']:
                data['direction'] = 'inflow'
            elif transaction_type in ['expense', 'outflow']:
                data['direction'] = 'outflow'
            else:
                return jsonify({"error": "Invalid transaction type. Use 'income' or 'expense'"}), 400
        elif 'type' in data and 'direction' in data:
            # If both are provided, prefer direction but warn if they conflict
            pass

        required_fields = ["date", "amount", "direction"]
        if not data or not all(field in data for field in required_fields):
            return jsonify(
                {"error": "date, amount, and direction are required"}
            ), 400

        # Auto-fill business_id from user's business
        business_id = data.get("business_id")

        business = None
        if business_id:
            # If business_id provided, verify it exists and user owns it
            business = Business.query.get(business_id)
            if not business:
                return jsonify({"error": "Business not found"}), 404
            
            if business.owner_id != g.current_user.id and g.current_user.role != "admin":
                return jsonify({"error": "You can only create transactions for your own business"}), 403
        else:
            # If no business_id provided, automatically find the user's business
            business = Business.query.filter_by(owner_id=g.current_user.id).first()
            if not business:
                return jsonify({"error": "No business found for this user. Please create a business profile first."}), 404
            # No ownership check needed here since we queried by owner_id

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

        # AI Anomaly Detection
        is_anomalous = data.get("is_anomalous", False)
        ai_tag = data.get("ai_tag")

        try:
            ai_service = AIService()
            analysis_data = {
                "description": data.get("description", ""),
                "amount": data["amount"],
                "date": str(transaction_date),
                "category": category.name if "category_id" in data and data["category_id"] else "Unknown",
                "direction": data["direction"]
            }
            
            ai_response = ai_service.analyze_transaction_anomaly(analysis_data)
            
            # Handle JSON response from AI Service
            if isinstance(ai_response, dict):
                if ai_response.get("is_anomalous"):
                    is_anomalous = True
                    ai_tag = ai_response.get("tag", "Anomalous")
            elif isinstance(ai_response, str):
                # Fallback for older text-based responses (just in case)
                if "unusual" in ai_response.lower() or "anomaly" in ai_response.lower():
                    is_anomalous = True
                    ai_tag = ai_response[:50]
            
        except Exception as e:
            print(f"AI Anomaly Detection Failed: {e}")
            # Fail silently, don't block transaction creation

        transaction = Transaction(
            business_id=business.id,
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
            is_anomalous=is_anomalous,
            ai_tag=ai_tag,
        )

        db.session.add(transaction)
        db.session.commit()

        # Automatically create an alert if anomalous
        if is_anomalous:
            alert = Alert(
                business_id=business.id,
                level="warning",
                message=f"Suspicious Transaction Detected: {transaction.description}",
                linked_transaction_id=transaction.id,
                forecast_metadata={"ai_reason": ai_tag}
            )
            db.session.add(alert)
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
        # Verify user is authenticated
        if not hasattr(g, 'current_user') or not g.current_user:
            return jsonify({"error": "Authentication required"}), 401

        # Only return transactions for businesses the user owns or if user is admin
        if g.current_user.role == "admin":
            transactions = Transaction.query.all()
        else:
            transactions = Transaction.query.join(Business).filter(Business.owner_id == g.current_user.id).all()

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
        # The transaction_access_required decorator handles authentication and authorization
        # Get the transaction from the g object, if available, otherwise query from db
        if hasattr(g, 'current_transaction') and g.current_transaction:
            transaction = g.current_transaction
        else:
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
        # The transaction_access_required decorator handles authentication and authorization
        # Get the transaction from the g object, if available, otherwise query from db
        if hasattr(g, 'current_transaction') and g.current_transaction:
            transaction = g.current_transaction
        else:
            transaction = Transaction.query.get(transaction_id)
            if not transaction:
                return jsonify({"error": "Transaction not found"}), 404

        data = request.get_json()

        # Note: business_id changes are not allowed for security reasons
        # Only admin can change the business association of a transaction
        if "business_id" in data and data["business_id"] != transaction.business_id:
            if not hasattr(g, 'current_user') or g.current_user.role != "admin":
                return jsonify({"error": "Cannot change business association of transaction"}), 403
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
        # The transaction_access_required decorator handles authentication and authorization
        # Get the transaction from the g object, if available, otherwise query from db
        if hasattr(g, 'current_transaction') and g.current_transaction:
            transaction = g.current_transaction
        else:
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

        # Verify user is authenticated
        if not hasattr(g, 'current_user') or not g.current_user:
            return jsonify({"error": "Authentication required"}), 401

        # Verify user owns this business or is an admin
        if business.owner_id != g.current_user.id and g.current_user.role != "admin":
            return jsonify({"error": "You can only view transactions for your own business"}), 403

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

        # Verify user is authenticated
        if not hasattr(g, 'current_user') or not g.current_user:
            return jsonify({"error": "Authentication required"}), 401

        # Verify user owns the business associated with this category
        if category.business.owner_id != g.current_user.id and g.current_user.role != "admin":
            return jsonify({"error": "You can only view transactions for your own business"}), 403

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
