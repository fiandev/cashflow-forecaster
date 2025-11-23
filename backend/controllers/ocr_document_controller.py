from flask import request, jsonify
from models import db, OCRDocument, Business, User
from decimal import Decimal


class OCRDocumentController:
    @staticmethod
    def create_ocr_document():
        data = request.get_json()

        if not data or not data.get("business_id"):
            return jsonify({"error": "business_id is required"}), 400

        business = Business.query.get(data["business_id"])
        if not business:
            return jsonify({"error": "Business not found"}), 404

        if "uploaded_by" in data and data["uploaded_by"]:
            user = User.query.get(data["uploaded_by"])
            if not user:
                return jsonify({"error": "User not found"}), 404

        ocr_document = OCRDocument(
            business_id=data["business_id"],
            uploaded_by=data.get("uploaded_by"),
            raw_text=data.get("raw_text"),
            parsed=data.get("parsed"),
            confidence=Decimal(str(data["confidence"]))
            if data.get("confidence")
            else None,
            source_image_url=data.get("source_image_url"),
        )

        db.session.add(ocr_document)
        db.session.commit()

        return jsonify(
            {
                "id": ocr_document.id,
                "business_id": ocr_document.business_id,
                "uploaded_by": ocr_document.uploaded_by,
                "uploaded_at": ocr_document.uploaded_at.isoformat()
                if ocr_document.uploaded_at
                else None,
                "raw_text": ocr_document.raw_text,
                "parsed": ocr_document.parsed,
                "confidence": float(ocr_document.confidence)
                if ocr_document.confidence
                else None,
                "source_image_url": ocr_document.source_image_url,
            }
        ), 201

    @staticmethod
    def get_ocr_documents():
        ocr_documents = OCRDocument.query.all()
        return jsonify(
            [
                {
                    "id": doc.id,
                    "business_id": doc.business_id,
                    "uploaded_by": doc.uploaded_by,
                    "uploaded_at": doc.uploaded_at.isoformat()
                    if doc.uploaded_at
                    else None,
                    "raw_text": doc.raw_text,
                    "parsed": doc.parsed,
                    "confidence": float(doc.confidence) if doc.confidence else None,
                    "source_image_url": doc.source_image_url,
                }
                for doc in ocr_documents
            ]
        )

    @staticmethod
    def get_ocr_document(document_id):
        ocr_document = OCRDocument.query.get(document_id)
        if not ocr_document:
            return jsonify({"error": "OCR document not found"}), 404

        return jsonify(
            {
                "id": ocr_document.id,
                "business_id": ocr_document.business_id,
                "uploaded_by": ocr_document.uploaded_by,
                "uploaded_at": ocr_document.uploaded_at.isoformat()
                if ocr_document.uploaded_at
                else None,
                "raw_text": ocr_document.raw_text,
                "parsed": ocr_document.parsed,
                "confidence": float(ocr_document.confidence)
                if ocr_document.confidence
                else None,
                "source_image_url": ocr_document.source_image_url,
            }
        )

    @staticmethod
    def update_ocr_document(document_id):
        ocr_document = OCRDocument.query.get(document_id)
        if not ocr_document:
            return jsonify({"error": "OCR document not found"}), 404

        data = request.get_json()

        if "business_id" in data:
            business = Business.query.get(data["business_id"])
            if not business:
                return jsonify({"error": "Business not found"}), 404
            ocr_document.business_id = data["business_id"]

        if "uploaded_by" in data:
            if data["uploaded_by"]:
                user = User.query.get(data["uploaded_by"])
                if not user:
                    return jsonify({"error": "User not found"}), 404
            ocr_document.uploaded_by = data["uploaded_by"]

        if "raw_text" in data:
            ocr_document.raw_text = data["raw_text"]

        if "parsed" in data:
            ocr_document.parsed = data["parsed"]

        if "confidence" in data:
            ocr_document.confidence = (
                Decimal(str(data["confidence"])) if data["confidence"] else None
            )

        if "source_image_url" in data:
            ocr_document.source_image_url = data["source_image_url"]

        db.session.commit()

        return jsonify(
            {
                "id": ocr_document.id,
                "business_id": ocr_document.business_id,
                "uploaded_by": ocr_document.uploaded_by,
                "uploaded_at": ocr_document.uploaded_at.isoformat()
                if ocr_document.uploaded_at
                else None,
                "raw_text": ocr_document.raw_text,
                "parsed": ocr_document.parsed,
                "confidence": float(ocr_document.confidence)
                if ocr_document.confidence
                else None,
                "source_image_url": ocr_document.source_image_url,
            }
        )

    @staticmethod
    def delete_ocr_document(document_id):
        ocr_document = OCRDocument.query.get(document_id)
        if not ocr_document:
            return jsonify({"error": "OCR document not found"}), 404

        db.session.delete(ocr_document)
        db.session.commit()

        return jsonify({"message": "OCR document deleted successfully"})

    @staticmethod
    def get_ocr_documents_by_business(business_id):
        business = Business.query.get(business_id)
        if not business:
            return jsonify({"error": "Business not found"}), 404

        ocr_documents = OCRDocument.query.filter_by(business_id=business_id).all()
        return jsonify(
            [
                {
                    "id": doc.id,
                    "business_id": doc.business_id,
                    "uploaded_by": doc.uploaded_by,
                    "uploaded_at": doc.uploaded_at.isoformat()
                    if doc.uploaded_at
                    else None,
                    "raw_text": doc.raw_text,
                    "parsed": doc.parsed,
                    "confidence": float(doc.confidence) if doc.confidence else None,
                    "source_image_url": doc.source_image_url,
                }
                for doc in ocr_documents
            ]
        )

    @staticmethod
    def get_ocr_documents_by_user(user_id):
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        ocr_documents = OCRDocument.query.filter_by(uploaded_by=user_id).all()
        return jsonify(
            [
                {
                    "id": doc.id,
                    "business_id": doc.business_id,
                    "uploaded_by": doc.uploaded_by,
                    "uploaded_at": doc.uploaded_at.isoformat()
                    if doc.uploaded_at
                    else None,
                    "raw_text": doc.raw_text,
                    "parsed": doc.parsed,
                    "confidence": float(doc.confidence) if doc.confidence else None,
                    "source_image_url": doc.source_image_url,
                }
                for doc in ocr_documents
            ]
        )
