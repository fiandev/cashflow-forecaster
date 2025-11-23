from models import OCRDocument, Business, User
from repositories.base_repository import BaseRepository
from typing import List, Optional, Dict, Any
from decimal import Decimal


class OCRDocumentRepository(BaseRepository):
    def __init__(self):
        super().__init__(OCRDocument)

    def findByBusiness(self, business_id: int) -> List[OCRDocument]:
        """Find OCR documents by business"""
        return self.find_by(business_id=business_id)

    def findByUploadedBy(self, user_id: int) -> List[OCRDocument]:
        """Find OCR documents by uploader"""
        return self.find_by(uploaded_by=user_id)

    def findByConfidenceRange(
        self, business_id: int, min_confidence: Decimal, max_confidence: Decimal
    ) -> List[OCRDocument]:
        """Find OCR documents by confidence range"""
        return self.model.query.filter(
            self.model.business_id == business_id,
            self.model.confidence >= min_confidence,
            self.model.confidence <= max_confidence,
        ).all()

    def findHighConfidence(
        self, business_id: int, threshold: Decimal = Decimal("0.9")
    ) -> List[OCRDocument]:
        """Find high confidence OCR documents"""
        return self.model.query.filter(
            self.model.business_id == business_id, self.model.confidence >= threshold
        ).all()

    def findLowConfidence(
        self, business_id: int, threshold: Decimal = Decimal("0.7")
    ) -> List[OCRDocument]:
        """Find low confidence OCR documents"""
        return self.model.query.filter(
            self.model.business_id == business_id, self.model.confidence < threshold
        ).all()

    def createWithBusiness(self, data: Dict[str, Any], business_id: int) -> OCRDocument:
        """Create OCR document with business"""
        ocr_data = data.copy()
        ocr_data["business_id"] = business_id
        return self.create(ocr_data)

    def createWithUploader(self, data: Dict[str, Any], user_id: int) -> OCRDocument:
        """Create OCR document with uploader"""
        ocr_data = data.copy()
        ocr_data["uploaded_by"] = user_id
        return self.create(ocr_data)

    def searchByRawText(self, business_id: int, query: str) -> List[OCRDocument]:
        """Search OCR documents by raw text"""
        return self.model.query.filter(
            self.model.business_id == business_id,
            self.model.raw_text.like(f"%{query}%"),
        ).all()

    def searchByParsedData(self, business_id: int, query: str) -> List[OCRDocument]:
        """Search OCR documents by parsed data"""
        return self.model.query.filter(
            self.model.business_id == business_id,
            db.cast(self.model.parsed, db.Text).like(f"%{query}%"),
        ).all()

    def getWithBusiness(self, ocr_id: int) -> Optional[OCRDocument]:
        """Get OCR document with business"""
        return (
            self.model.query.options(db.joinedload(self.model.business))
            .filter_by(id=ocr_id)
            .first()
        )

    def getWithUploader(self, ocr_id: int) -> Optional[OCRDocument]:
        """Get OCR document with uploader"""
        return (
            self.model.query.options(db.joinedload(self.model.uploaded_by_user))
            .filter_by(id=ocr_id)
            .first()
        )

    def getWithTransactions(self, ocr_id: int) -> Optional[OCRDocument]:
        """Get OCR document with transactions"""
        return (
            self.model.query.options(db.joinedload(self.model.transactions))
            .filter_by(id=ocr_id)
            .first()
        )

    def getWithAllRelations(self, ocr_id: int) -> Optional[OCRDocument]:
        """Get OCR document with all relationships"""
        return (
            self.model.query.options(
                db.joinedload(self.model.business),
                db.joinedload(self.model.uploaded_by_user),
                db.joinedload(self.model.transactions),
            )
            .filter_by(id=ocr_id)
            .first()
        )

    def getAverageConfidence(self, business_id: int) -> Optional[Decimal]:
        """Get average confidence score for business"""
        return (
            db.session.query(db.func.avg(self.model.confidence))
            .filter_by(business_id=business_id)
            .scalar()
        )

    def getDocumentsWithoutTransactions(self, business_id: int) -> List[OCRDocument]:
        """Get OCR documents that haven't generated transactions"""
        return self.model.query.filter(
            self.model.business_id == business_id, ~self.model.transactions.any()
        ).all()

    def getRecentDocuments(self, business_id: int, days: int = 30) -> List[OCRDocument]:
        """Get recent OCR documents"""
        from datetime import datetime, timedelta

        cutoff_date = datetime.utcnow() - timedelta(days=days)
        return self.model.query.filter(
            self.model.business_id == business_id, self.model.uploaded_at >= cutoff_date
        ).all()
