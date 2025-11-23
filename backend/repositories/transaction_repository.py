from models import Transaction, Business, Category, OCRDocument
from repositories.base_repository import BaseRepository
from typing import List, Optional, Dict, Any
from datetime import datetime, date
from decimal import Decimal


class TransactionRepository(BaseRepository):
    def __init__(self):
        super().__init__(Transaction)

    def findByBusiness(self, business_id: int) -> List[Transaction]:
        """Find transactions by business"""
        return self.find_by(business_id=business_id)

    def findByCategory(self, category_id: int) -> List[Transaction]:
        """Find transactions by category"""
        return self.find_by(category_id=category_id)

    def findByDirection(self, direction: str) -> List[Transaction]:
        """Find transactions by direction (inflow/outflow)"""
        return self.find_by(direction=direction)

    def findByDateRange(
        self, business_id: int, start_date: date, end_date: date
    ) -> List[Transaction]:
        """Find transactions within date range"""
        return self.model.query.filter(
            self.model.business_id == business_id,
            self.model.date >= start_date,
            self.model.date <= end_date,
        ).all()

    def findByAmountRange(
        self, business_id: int, min_amount: Decimal, max_amount: Decimal
    ) -> List[Transaction]:
        """Find transactions within amount range"""
        return self.model.query.filter(
            self.model.business_id == business_id,
            self.model.amount >= min_amount,
            self.model.amount <= max_amount,
        ).all()

    def findAnomalous(self, business_id: int) -> List[Transaction]:
        """Find anomalous transactions"""
        return self.model.query.filter_by(
            business_id=business_id, is_anomalous=True
        ).all()

    def findBySource(self, source: str) -> List[Transaction]:
        """Find transactions by source"""
        return self.find_by(source=source)

    def findByOCRDocument(self, ocr_document_id: int) -> List[Transaction]:
        """Find transactions by OCR document"""
        return self.find_by(ocr_document_id=ocr_document_id)

    def createWithBusiness(self, data: Dict[str, Any], business_id: int) -> Transaction:
        """Create transaction with business"""
        transaction_data = data.copy()
        transaction_data["business_id"] = business_id
        return self.create(transaction_data)

    def createWithCategory(self, data: Dict[str, Any], category_id: int) -> Transaction:
        """Create transaction with category"""
        transaction_data = data.copy()
        transaction_data["category_id"] = category_id
        return self.create(transaction_data)

    def search(self, business_id: int, query: str) -> List[Transaction]:
        """Search transactions by description"""
        return self.model.query.filter(
            self.model.business_id == business_id,
            self.model.description.like(f"%{query}%"),
        ).all()

    def getWithCategory(self, transaction_id: int) -> Optional[Transaction]:
        """Get transaction with category"""
        return (
            self.model.query.options(db.joinedload(self.model.category))
            .filter_by(id=transaction_id)
            .first()
        )

    def getWithBusiness(self, transaction_id: int) -> Optional[Transaction]:
        """Get transaction with business"""
        return (
            self.model.query.options(db.joinedload(self.model.business))
            .filter_by(id=transaction_id)
            .first()
        )

    def getWithOCRDocument(self, transaction_id: int) -> Optional[Transaction]:
        """Get transaction with OCR document"""
        return (
            self.model.query.options(db.joinedload(self.model.ocr_document))
            .filter_by(id=transaction_id)
            .first()
        )

    def getWithAlerts(self, transaction_id: int) -> Optional[Transaction]:
        """Get transaction with alerts"""
        return (
            self.model.query.options(db.joinedload(self.model.alerts))
            .filter_by(id=transaction_id)
            .first()
        )

    def getWithAllRelations(self, transaction_id: int) -> Optional[Transaction]:
        """Get transaction with all relationships"""
        return (
            self.model.query.options(
                db.joinedload(self.model.business),
                db.joinedload(self.model.category),
                db.joinedload(self.model.ocr_document),
                db.joinedload(self.model.alerts),
            )
            .filter_by(id=transaction_id)
            .first()
        )

    def getIncomeTransactions(self, business_id: int) -> List[Transaction]:
        """Get income transactions for business"""
        return self.model.query.filter_by(
            business_id=business_id, direction="inflow"
        ).all()

    def getExpenseTransactions(self, business_id: int) -> List[Transaction]:
        """Get expense transactions for business"""
        return self.model.query.filter_by(
            business_id=business_id, direction="outflow"
        ).all()

    def getTotalByDateRange(
        self, business_id: int, start_date: date, end_date: date
    ) -> Dict[str, Decimal]:
        """Get total inflow and outflow by date range"""
        inflow_total = db.session.query(db.func.sum(self.model.amount)).filter(
            self.model.business_id == business_id,
            self.model.date >= start_date,
            self.model.date <= end_date,
            self.model.direction == "inflow",
        ).scalar() or Decimal("0")

        outflow_total = db.session.query(db.func.sum(self.model.amount)).filter(
            self.model.business_id == business_id,
            self.model.date >= start_date,
            self.model.date <= end_date,
            self.model.direction == "outflow",
        ).scalar() or Decimal("0")

        return {
            "inflow": inflow_total,
            "outflow": outflow_total,
            "net": inflow_total - outflow_total,
        }
